import React, { useState } from "react";

function NewPostForm({ onPost }) {
  const [author, setAuthor] = useState("");
  const [message, setMessage] = useState("");

  const colors = ["#FFFA65", "#FFB347", "#9EE09E", "#FFA3A3", "#86d1f7ff", "#be9aeaff", "#8bf1f8ff", "#fa7ac9ff"];
  const rotations = [-15, 13.2, 1.5, -11.7, 3, 7, -0.6];

  const submit = async (e) => {
    e.preventDefault();
    if (!author || !message) return;

    try {
      const res = await fetch("/api/post", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ author, message })
      });

      const newPost = await res.json();

      onPost({
        ...newPost,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: (Math.random() - 0.5) * 20
      });

      setAuthor("");
      setMessage("");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ position: "relative", width: "200px", height: "200px" }}>
      {colors.slice(1).map((color, i) => {
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              width: "200px",
              height: "200px",
              backgroundColor: color,
              boxShadow: "2px 2px 5px rgba(0,0,0,0.3)",
              transform: `rotate(${rotations[i]}deg)`,
              zIndex: i
            }}
          />
        );
      })}
      <form
        onSubmit={submit}
        style={{
          position: "relative",
          zIndex: colors.length,
          width: "200px",
          height: "200px",
          backgroundColor: colors[0],
          padding: "0.5rem",
          boxShadow: "2px 2px 5px rgba(0,0,0,0.3)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <input
          placeholder="Author"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          style={{
            padding: "0.25rem",
            fontFamily: "'Patrick Hand', cursive",
            fontSize: "1rem"
          }}
        />
        <textarea
          placeholder="Message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{
            padding: "0.25rem",
            fontFamily: "'Patrick Hand', cursive",
            fontSize: "1rem",
            resize: "none",
            flexGrow: 1
          }}
        />
        <button
          type="submit"
          style={{
            marginTop: "0.25rem",
            padding: "0.25rem",
            fontFamily: "'Patrick Hand', cursive",
            cursor: "pointer"
          }}
        >
          Post
        </button>
      </form>
    </div>
  );
}

export default NewPostForm;
