import React from 'react';
import { Attempt } from '../interfaces/Attempt';
import { City } from '../interfaces/City';
import { Temperature } from './Temperature';

const CANVAS_WIDTH = 1600
const CANVAS_HEIGHT = 1600
const CITY_RADIUS = 10
const STROKE_WIDTH = 3
const colors = ["rgba(0, 0, 0, 0.5)", "rgba(255, 0, 0, 0.5)", "rgba(0, 255, 0, 0.5)", "rgba(0, 0, 255, 0.5)", "rgba(255, 0, 255, 0.5)"]

interface GraphProps {data: Attempt[]}

interface GraphState {attemptIndex: number}

export class Graph extends React.Component<GraphProps, GraphState> {
    private canvas;

    constructor(props: any) {
        super(props);
        this.state = {
            attemptIndex: 0,
        };
        this.canvas = React.createRef<HTMLCanvasElement>();
    }

    private getEdgeCoordinates(attempt: Attempt): {maxX: number, minX: number, maxY: number, minY: number} {
        const result = {
            maxX: -Infinity,
            minX: Infinity,
            maxY: -Infinity,
            minY: Infinity,
        }

        attempt.paths.forEach((path: City[]) => {
            path.forEach((city: City) => {
                if (city.x > result.maxX) result.maxX = city.x;
                if (city.x < result.minX) result.minX = city.x;
                if (city.y > result.maxY) result.maxY = city.y;
                if (city.y < result.minY) result.minY = city.y;
            })
        })

        return result
    }

    private scaleCoordsToCanvas(attempt: Attempt): Attempt {
        const attemptCopy = JSON.parse(JSON.stringify(attempt));
        const edgeCoordinates = this.getEdgeCoordinates(attemptCopy);
        console.log({edgeCoordinates})
        
        attemptCopy.paths.forEach((path: City[]) => {
            path.forEach((city: City) => {
                city.x = (city.x - edgeCoordinates.minX) / (edgeCoordinates.maxX - edgeCoordinates.minX) * CANVAS_WIDTH;
                city.y = (city.y - edgeCoordinates.minY) / (edgeCoordinates.maxY - edgeCoordinates.minY) * CANVAS_HEIGHT;
            })
        })

        return attemptCopy;
    }

    private drawAttempt = (attempt: Attempt) => {
        const ctx = this?.canvas?.current?.getContext('2d')
        if (!ctx || !attempt) {
            return
        }
        ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

        const scaledAttempt = this.scaleCoordsToCanvas(attempt);
        console.log(scaledAttempt.paths)

        scaledAttempt.paths.forEach((path: City[], index: number) => {
            path.forEach((city: City) => {
                this.drawCity(ctx, city);
            })
            this.drawPath(ctx, path, colors[index]);
        })



    }

    private drawCity(ctx: CanvasRenderingContext2D, city: City): void {
        if (city.city === "Kraków") {
            ctx.fillStyle = 'red';
        } else {
            ctx.fillStyle = 'black';
        }
        ctx.beginPath();
        ctx.ellipse(city.x, city.y, CITY_RADIUS, CITY_RADIUS, Math.PI / 4, 0, 2 * Math.PI);
        ctx.fill();
    }

    private drawPath(ctx: CanvasRenderingContext2D, path: City[], color: string): void {
        for(let i = 0; i < path.length - 1; i++) {
            ctx.strokeStyle = color;
            ctx.beginPath();       // Start a new path
            ctx.moveTo(path[i].x, path[i].y);    // Move the pen to (30, 50)
            ctx.lineTo(path[i + 1].x, path[i + 1].y);  // Draw a line to (150, 100)
            ctx.lineWidth = STROKE_WIDTH;
            ctx.stroke();          // Render the path
        }
    }

    private getEdgeTemperatures(): {min: number, max: number} {
        const result = {min: Infinity, max: -Infinity};

        this.props.data.forEach((attempt: Attempt) => {
            if (attempt.temp < result.min) result.min = attempt.temp;
            if (attempt.temp > result.max) result.max = attempt.temp;
        })

        return result;
    }

    private getAttemptFitness(attempt: Attempt): number {
        let total = 0;

        attempt.paths.forEach((path: City[]) => {
            for(let i = 0; i < path.length; i++) {
                const city1 = path[i];
                const city2 = path[(i + 1) % path.length];
                total += Math.sqrt((city2.x-city1.x) ** 2 + (city2.y - city2.x) ** 2);
            }
        })

        return total;
    }

    render() {
        const {data} = this.props;
        const {attemptIndex} = this.state

        const edgeTemperatures = this.getEdgeTemperatures();
        const currentAttempt = data ? data[attemptIndex] : null;

        return (
            <div>
                <div>
                    <input
                        type="range"
                        id="attempt"
                        name="attempt"
                        min="0"
                        max={data.length - 1}
                        value={attemptIndex}
                        onChange={(event) => {
                            const newIndex = Number(event.target.value);
                            this.setState({attemptIndex: newIndex});
                            this.drawAttempt(data[newIndex]);
                        }}
                    />
                    <label htmlFor="attempt">Attempt</label>
                </div>
                <button
                    onClick={() => this.setState((prevState) => {
                        this.drawAttempt(data[prevState.attemptIndex + 1]);
                        return ({attemptIndex: prevState.attemptIndex + 1})
                    })}
                >
                    Next step
                </button>
                <br />
                <Temperature
                    maxTemperautre={edgeTemperatures.max}
                    minTemperature={edgeTemperatures.min}
                    currentTemperature={currentAttempt ? currentAttempt.temp : 0}
                />
                <div>
                    Total distance {currentAttempt ? this.getAttemptFitness(currentAttempt).toFixed(2) : 0}
                </div>
                <br />
                <div>
                    <canvas width={CANVAS_WIDTH} height={CANVAS_HEIGHT} ref={this.canvas}></canvas>
                </div>
            </div>
        );
    }
}
