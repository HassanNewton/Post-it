import React, { useState, useEffect } from "react";
import PostIt from "./components/PostIt";
import NewPostForm from "./components/NewPostForm";

function App() {
  
  const colors = ["#FFFA65", "#FFB347", "#9EE09E", "#FFA3A3", "#86d1f7ff", "#be9aeaff", "#8bf1f8ff", "#fa7ac9ff"];

  const [posts, setPosts] = useState([]);

  useEffect(() => {
    async function fetchPosts() {
      try {
        const res = await fetch("/api/posts");
        const data = await res.json();

        const styledPosts = data.map(post => ({
          ...post,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: (Math.random() - 0.5) * 20
        }));

        setPosts(styledPosts);
      } catch (err) {
        console.error("Error fetching posts:", err);
      }
    }

    fetchPosts();
  }, []);

  const addPost = (post) => {
    setPosts([post, ...posts]);
  };

  return (
    <div style={{ padding: "2rem", minHeight: "100vh" }}>
      <div style={{
        display: "flex",
        justifyContent: "flex-start",
        alignItems: "center",
        gap: "3rem",
        marginBottom: "5rem"
      }}>
        <h1 style={{
          fontFamily: "'Fredoka One', cursive",
          fontSize: "7rem",
          margin: 0,
          lineHeight: 1
        }}>
          Post It
        </h1>
        <NewPostForm onPost={addPost} />
      </div>

      <div style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "3rem",
        justifyContent: "center",
        alignItems: "center"
      }}>
        {posts.map(post => (
          <PostIt 
            key={post.id} 
            author={post.author} 
            message={post.message} 
            color={colors[Math.floor(Math.random() * colors.length)]} 
            rotation={(Math.random() - 0.5) * 20}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
