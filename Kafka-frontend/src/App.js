//import logo from './logo.svg';
import './App.css';
import Filetypecsv from './components/Filetypecsv';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";

import Filetypeapi from './components/Filetypeapi';
import Filetypeparquet from './components/Filetypeparquet';
function App() {
  return (
    <Router>
    
    <Routes>
      <Route exact path="/" element={<Filetypecsv/>} />
      <Route exact path="/Filetypeapi" element={<Filetypeapi/>} />
      <Route exact path="/Filetypeparquet" element={<Filetypeparquet/>} />
      {/* Add more Routes as needed */}
    </Routes>
  </Router>
 
   
  );
}

export default App;
