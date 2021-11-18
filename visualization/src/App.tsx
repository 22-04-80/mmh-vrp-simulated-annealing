import React from 'react';
import {Graph} from "./graph/Graph";
import { Attempt } from './interfaces/Attempt';

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
      const text = (e?.target?.result)
      console.log(text)
      this.setState({data: JSON.parse(text as string)})
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
