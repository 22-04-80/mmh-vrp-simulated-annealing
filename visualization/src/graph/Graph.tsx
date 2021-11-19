import React from 'react';
import { Attempt } from '../interfaces/Attempt';
import { City } from '../interfaces/City';
import { Temperature } from './Temperature';
import "./graph.css";

const CANVAS_WIDTH = 800
const CANVAS_HEIGHT = 800
const CITY_RADIUS = 10
const STROKE_WIDTH = 3
const colors = ["rgba(0, 0, 0, 0.5)", "rgba(255, 0, 0, 0.5)", "rgba(0, 255, 0, 0.5)", "rgba(0, 0, 255, 0.5)", "rgba(255, 0, 255, 0.5)"]
const SIMULATION_STEP_INTERVAL_MS = 300

interface GraphProps {data: Attempt[]}

interface GraphState {
    attemptIndex: number;
    interval: NodeJS.Timeout | null;
}

export class Graph extends React.Component<GraphProps, GraphState> {
    private canvas;

    constructor(props: any) {
        super(props);

        this.state = {
            attemptIndex: 0,
            interval: null,
        };
        this.canvas = React.createRef<HTMLCanvasElement>();
    }

    componentDidUpdate(prevProps: GraphProps) {
        if (prevProps.data.length === 0 && this.props.data.length !== 0) {
            this.drawAttempt(this.props.data[this.state.attemptIndex]);
        }
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

        scaledAttempt.paths.forEach((path: City[], index: number) => {
            path.forEach((city: City) => {
                this.drawCity(ctx, city);
            })
            this.drawPath(ctx, path, colors[index]);
        });
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
            ctx.beginPath();
            ctx.moveTo(path[i].x, path[i].y);
            ctx.lineTo(path[i + 1].x, path[i + 1].y);
            ctx.lineWidth = STROKE_WIDTH;
            ctx.stroke();
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

    private showNextStep = () => {
        const {data} = this.props;

        this.setState((prevState) => {
            this.drawAttempt(data[prevState.attemptIndex + 1]);
            return ({attemptIndex: prevState.attemptIndex + 1})
        })
    }

    private startSimulation: () => void = () => {
        if (this.state.interval) {
            return;
        }

        const interval = setInterval(() => {
            if (this.state.attemptIndex >= this.props.data.length) {
                this.stopSimulation();
            } else {
                this.showNextStep()
            }
        }, SIMULATION_STEP_INTERVAL_MS);
        this.setState({interval});
    }

    private stopSimulation: () => void = () => {
        const {interval} = this.state;
        if (interval) {
            clearInterval(interval);
            this.setState({interval: null});
        }
    }

    private isSimulationRunning: () => boolean = () => {
        return Boolean(this.state.interval);
    }

    private goToBestAttempt: () => void = () => {
        const {data} = this.props;
        let bestResultIndex: number = 0;
        let bestResultFitness: number = data[bestResultIndex].current_value;

        data.forEach((attempt: Attempt, index: number) => {
            if (attempt.current_value < bestResultFitness) {
                bestResultFitness = attempt.current_value;
                bestResultIndex = index;
            }
        });

        this.setState(() => {
            this.drawAttempt(data[bestResultIndex]);
            return ({attemptIndex: bestResultIndex});
        });
    }

    render() {
        const {data} = this.props;
        const {attemptIndex} = this.state

        const edgeTemperatures = this.getEdgeTemperatures();
        const currentAttempt = data ? data[attemptIndex] : null;

        return (
            <div className="container">
                <div className="content">
                    <canvas width={CANVAS_WIDTH} height={CANVAS_HEIGHT} ref={this.canvas}></canvas>
                </div>
                <div className="controls">
                    <div>
                        <button
                            disabled={this.isSimulationRunning()}
                            onClick={this.startSimulation}
                        >
                            Start simulation
                        </button>
                        <button
                            disabled={!this.isSimulationRunning()}
                            onClick={this.stopSimulation}
                        >
                            Stop simulation
                        </button>
                    </div>
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
                    <button onClick={this.showNextStep}>
                        Next step
                    </button>
                    <button onClick={this.goToBestAttempt}>
                        Show best result
                    </button>
                    <div>
                        Current epoch: {currentAttempt?.epoch}
                    </div>
                    <div>
                        Current attempt: {currentAttempt?.attempt}
                    </div>
                    <Temperature
                        maxTemperautre={edgeTemperatures.max}
                        minTemperature={edgeTemperatures.min}
                        currentTemperature={currentAttempt?.temp || 0}
                    />
                    <div>
                        Current distance {currentAttempt?.current_value.toFixed(2) || 0}
                    </div>
                    <div>
                        Best known distance {currentAttempt?.current_best_known_value.toFixed(2) || 0}
                    </div>
                </div>
            </div>
        );
    }
}
