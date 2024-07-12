import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import LoginForm from "../components/LoginForm.jsx";
import PhotoForm from "../components/PhotoForm.jsx";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { Link } from "react-router-dom";

export const Home = () => {

  const {store, dispatch} =useGlobalReducer()

	return (
		<div className="text-center mt-5">
			<LoginForm />
			<PhotoForm />
			<Link className="btn btn-primary" to="/private">
				Visit the private page.
			</Link>
			{JSON.stringify(store)}
		</div>
	);
}; 