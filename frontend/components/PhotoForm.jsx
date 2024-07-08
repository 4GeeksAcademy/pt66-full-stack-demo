import React, { useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

const PhotoForm = () => {
  const { store, dispatch } = useGlobalReducer();

  const [url, setUrl] = useState("");

  const handleSubmit = async (ev) => {
    ev.preventDefault();

    const resp = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/photos`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${store.token}`
      },
      body: JSON.stringify({
        url,
      }),
    });

    if (resp.ok) {
      const resp = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/users/current`, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${store.token}`
        },
      })

      if (resp.ok) {
        const data = await resp.json();
        dispatch({
          user: data,
          type: 'update_user'
        });
      }
      setUrl("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="d-flex flex-column gap-3 p-3">
      <input
        type="text"
        value={url}
        onChange={(ev) => setUrl(ev.target.value)}
        placeholder="photo url"
      />
      <button className="btn btn-primary">Submit Photo</button>
    </form>
  );
};

export default PhotoForm
