import {City} from "./City"

export interface Attempt {
    epoch: number;
    attempt: number;
    temp: number;
    paths: City[][];
}