import React from 'react';
import {Graph} from "./graph/Graph";
import { Attempt } from './interfaces/Attempt';
import { City } from './interfaces/City';

interface AppState {data: Attempt[]}

class App extends React.Component<any, AppState> {
  constructor(props: any) {
    super(props)
    this.state = {
      data: [],
    }
  }

  private showFile = async (e: any) => {
    e.preventDefault()
    const reader = new FileReader()
    reader.onload = async (e) => { 
      const fileContent = (e?.target?.result)
      const data: Attempt[] = JSON.parse(fileContent as string)
      const preparedData = data.map((attempt: Attempt) => {
        attempt.paths = attempt.paths.map((path: City[]) => {
          return path.map((city: City) => {
            city.y = -city.y;
            return city;
          })
        });
        return attempt;
      })
      this.setState({data: preparedData})
    };
    reader.readAsText(e?.target?.files[0])
  }

  render() {
    return (
      <div className="App">
        <input type="file" name="file" id="file" accept=".json" onChange={(event) => this.showFile(event)} />
        <Graph data={this.state.data}/>
      </div>
    );
  }
}

export default App;
