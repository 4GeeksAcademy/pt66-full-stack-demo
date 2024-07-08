import React, { useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

const LoginForm = () => {
  const { store, dispatch } = useGlobalReducer();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (ev) => {
    ev.preventDefault();

    const resp = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    if (resp.ok) {
      const data = await resp.json();
      dispatch({
        ...data,
        type: 'update_token'
      })
    }
  };

  return (
    <form onSubmit={handleSubmit} className="d-flex flex-column gap-3 p-3">
      <input
        type="text"
        value={username}
        onChange={(ev) => setUsername(ev.target.value)}
        placeholder="username"
      />
      <input
        type="password"
        value={password}
        onChange={(ev) => setPassword(ev.target.value)}
        placeholder="password"
      />
      <button className="btn btn-primary">Login</button>
    </form>
  );
};

export default LoginForm
