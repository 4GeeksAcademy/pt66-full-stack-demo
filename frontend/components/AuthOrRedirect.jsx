import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

const AuthOrRedirect = ({to, children}) => {
    const { store } = useGlobalReducer();
    const nav = useNavigate();

    useEffect(() => {
        if (!store.token) {
            console.log("Ding!");
            nav(to ? to : "/");
        }
    }, []);

    return <>
        {children}
    </>
}

export { AuthOrRedirect };
