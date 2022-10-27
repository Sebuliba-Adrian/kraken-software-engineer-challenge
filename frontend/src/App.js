import ApplicationContainer from "./ApplicationContainer";
import Navbar from "./Navbar";

function App() {
  return (
    <div className="App">
      <Navbar />
      <div className="content">
        <ApplicationContainer />
      </div>
    </div>
  );
}

export default App;
