import { useState } from "react";
import MainLayout from "../layout/MainLayout";
import "../styles/Banking.css";

function Deposit() {

  const user = JSON.parse(localStorage.getItem("user"));

  const [amount, setAmount] = useState("");
  const [remarks, setRemarks] = useState("");

  const handleDeposit = async () => {

    const response = await fetch("http://127.0.0.1:5000/deposit", {

      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({

        email: user.email,
        amount,
        remarks

      })

    });

    const data = await response.json();

    alert(data.message);

    setAmount("");
    setRemarks("");

  };

  return (

    <MainLayout>

      <div className="bank-card">

        <h2>💰 Deposit Money</h2>

        <input
          className="bank-input"
          type="number"
          placeholder="Deposit Amount"
          value={amount}
          onChange={(e)=>setAmount(e.target.value)}
        />

        <textarea
          className="bank-input"
          rows="3"
          placeholder="Remarks"
          value={remarks}
          onChange={(e)=>setRemarks(e.target.value)}
        />

        <button
          className="bank-btn"
          onClick={handleDeposit}
        >
          Deposit
        </button>

      </div>

    </MainLayout>

  );

}

export default Deposit;