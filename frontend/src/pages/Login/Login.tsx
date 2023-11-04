import { Link } from "react-router-dom";
import { PATHS } from "../../constants";

const Login = () => {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to={PATHS.HOME}>Home</Link>
          </li>
          <li>
            <Link to={PATHS.ABOUT}>About</Link>
          </li>
          <li>
            <Link to={PATHS.LOGIN}>login</Link>
          </li>
        </ul>
      </nav>
      <h1>Login</h1>
    </div>
  );
};

export default Login;
