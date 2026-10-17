import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Splash() {

  const navigate = useNavigate();

  useEffect(() => {

    const timer = setTimeout(() => {

      navigate("/welcome");

    },3000);

    return ()=>clearTimeout(timer);

  },[]);

  return(

    <div style={{
      height:"100vh",
      display:"flex",
      justifyContent:"center",
      alignItems:"center",
      flexDirection:"column",
      background:"#0A3D62",
      color:"white"
    }}>

      <h1>🏦 SecureBank AI</h1>

      <h2>Initializing AI Engine...</h2>

    </div>

  );

}

export default Splash;