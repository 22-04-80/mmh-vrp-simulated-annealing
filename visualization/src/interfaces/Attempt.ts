import {City} from "./City"

export interface Attempt {
    epoch: number;
    attempt: number;
    temp: number;
    paths: City[][];
    current_value: number;
    current_best_known_value: number;
    best_attempt_value: number;
}