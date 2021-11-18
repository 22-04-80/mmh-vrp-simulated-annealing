import React from "react";

interface TemperatureProps {
    minTemperature: number;
    maxTemperautre: number;
    currentTemperature: number;
}

export class Temperature extends React.Component <TemperatureProps, any> {
    render() {
        const {minTemperature, maxTemperautre, currentTemperature} = this.props;
        return (
            <div>
                Temperature:
                <progress
                    id="temperature"
                    max={maxTemperautre - minTemperature}
                    value={currentTemperature}
                >
                    {currentTemperature}
                </progress>
            </div>
        )
    }
}
