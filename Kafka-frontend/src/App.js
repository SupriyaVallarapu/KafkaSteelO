//import logo from './logo.svg';
import './App.css';
import Filetypecsv from './components/Filetypecsv';
//import Filetypelog from './components/Filetypelog';
import Filetypeparquet from './components/Filetypeparquet';
function App() {
  return (
    <div className="App">
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
      <h4>Parquet Filetype</h4>
<Filetypeparquet/>{/* <Filetypecsv/> */}

{/* <h4>Log Filetype</h4>
      <Filetypelog/> */}
    </div>
  );
}

export default App;
