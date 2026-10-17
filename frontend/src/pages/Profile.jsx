import { useEffect, useState } from "react";
import MainLayout from "../layout/MainLayout";
import "../styles/Banking.css";

function Profile() {

  const user = JSON.parse(localStorage.getItem("user"));

  const [profile, setProfile] = useState({
    name: "",
    email: "",
    phone: "",
    address: "",
  });

  useEffect(() => {

    fetch(`http://127.0.0.1:5000/profile/${user.email}`)
      .then((res) => res.json())
      .then((data) => setProfile(data));

  }, []);

  const handleSave = async () => {

    try {

      const response = await fetch("http://127.0.0.1:5000/profile", {

        method: "PUT",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(profile),

      });

      const data = await response.json();

      alert(data.message);

      // Update localStorage name
      const currentUser = JSON.parse(localStorage.getItem("user"));

      currentUser.name = profile.name;

      localStorage.setItem(
        "user",
        JSON.stringify(currentUser)
      );

    } catch (err) {

      console.log(err);

      alert("Server Error");

    }

  };

  return (

    <MainLayout>

      <div className="bank-card">

        <h2>👤 My Profile</h2>

        <div className="profile-row">

          <label>Name</label>

          <input
            className="bank-input"
            value={profile.name}
            onChange={(e) =>
              setProfile({
                ...profile,
                name: e.target.value,
              })
            }
          />

        </div>

        <div className="profile-row">

          <label>Email</label>

          <input
            className="bank-input"
            value={profile.email}
            readOnly
          />

        </div>

        <div className="profile-row">

          <label>Phone</label>

          <input
            className="bank-input"
            value={profile.phone || ""}
            onChange={(e) =>
              setProfile({
                ...profile,
                phone: e.target.value,
              })
            }
          />

        </div>

        <div className="profile-row">

          <label>Address</label>

          <textarea
            className="bank-input"
            rows="3"
            value={profile.address || ""}
            onChange={(e) =>
              setProfile({
                ...profile,
                address: e.target.value,
              })
            }
          />

        </div>

        <button
          className="bank-btn"
          onClick={handleSave}
        >
          Save Changes
        </button>

      </div>

    </MainLayout>

  );

}

export default Profile;