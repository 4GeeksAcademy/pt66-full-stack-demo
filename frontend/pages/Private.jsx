import { AuthOrRedirect } from "../components/AuthOrRedirect.jsx";

export const Private = () => {

	return (
		<AuthOrRedirect>
			<div className="text-center mt-5">
				Hello world!
			</div>
		</AuthOrRedirect>
	);
}; 