//import logo from './logo.svg';
import './App.css';
import Filetypecsv from './components/Filetypecsv';
import 'bootstrap/dist/css/bootstrap.min.css';
//import Filetypelog from './components/Filetypelog';
//import Filetypeparquet from './components/Filetypeparquet';
function App() {
  return (
    <div className="App">
      {/* <header className="App-header"
      </header> */}
      
{/* <Filetypeparquet/>
 */}
 <Filetypecsv/>
{/* <h4>Log Filetype</h4>
      <Filetypelog/> */}
    </div>
  );
}

export default App;
