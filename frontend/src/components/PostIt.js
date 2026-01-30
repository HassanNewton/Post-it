import React from "react";

function PostIt({ author, message, color, rotation }) {
  return (
    <div style={{
      position: "relative",
      width: "200px",
      height: "200px",
      padding: "1rem",
      border: `3px solid ${color}`,
      borderRadius: "0px",
      boxShadow: "2px 2px 5px rgba(0,0,0,0.3)",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      fontFamily: "'Patrick Hand', cursive",
      transform: `rotate(${rotation}deg)`,
      backgroundColor: color
    }}>
      <div style={{
        position: "absolute",
        top: "8px",
        left: "50%",
        transform: "translateX(-50%)",
        width: "12px",
        height: "12px",
        backgroundColor: "red",
        borderRadius: "50%"
      }} />
      <div>{message}</div>
      <small>- {author}</small>
    </div>
  );
}

export default PostIt;
