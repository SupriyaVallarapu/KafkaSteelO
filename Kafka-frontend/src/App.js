//import logo from './logo.svg';
import './App.css';
import Filetypecsv from './components/Filetypecsv';
import 'bootstrap/dist/css/bootstrap.min.css';
import Persistdataform from './components/Persistdataform';
import Postgresconnector from './components/Postgresconnector';
import Opcua from './components/Opcua';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";

import Filetypeapi from './components/Filetypeapi';
import Filetypeparquet from './components/Filetypeparquet';
function App() {
  return (
    <Router>
    
    <Routes>
    <Route exact path="/" element={<Filetypecsv/>} />
      <Route exact path="/Filetypecsv" element={<Filetypecsv/>} />
      <Route exact path="/Filetypeapi" element={<Filetypeapi/>} />
      <Route exact path="/Filetypeparquet" element={<Filetypeparquet/>} />
      <Route exact path="/Persistdataform" element={<Persistdataform/>} />
      <Route exact path="/Opcua" element={<Opcua/>} />
      <Route exact path="/Postgresconnector" element={<Postgresconnector/>} />
      {/* Add more Routes as needed */}
    </Routes>
  </Router>
 
   
  );
}

export default App;
