import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import LoginForm from "../components/LoginForm.jsx";
import PhotoForm from "../components/PhotoForm.jsx";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {

  const {store, dispatch} =useGlobalReducer()

	return (
		<div className="text-center mt-5">
			<LoginForm />
			<PhotoForm />
			{JSON.stringify(store)}
		</div>
	);
}; 