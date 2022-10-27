import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1>App meta data application</h1>
      <div className="links">
      <a href="/">Main</a>
      <a href="/create">New App</a>
      </div>
    </nav>
  );
}
 
export default Navbar;