import { useState } from "react";
import MainLayout from "../layout/MainLayout";
import "../styles/Banking.css";

function Transfer() {

  const user = JSON.parse(localStorage.getItem("user"));

  const [recipient, setRecipient] = useState("");
  const [account, setAccount] = useState("");
  const [ifsc, setIfsc] = useState("");
  const [amount, setAmount] = useState("");
  const [remarks, setRemarks] = useState("");

  const handleTransfer = async () => {

    if (
      !recipient ||
      !account ||
      !ifsc ||
      !amount
    ) {
      alert("Please fill all required fields.");
      return;
    }

    try {

      const response = await fetch(
        "http://127.0.0.1:5000/transfer",
        {

          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            email: user.email,

            recipient,

            account,

            ifsc,

            amount,

            remarks,

          }),

        }
      );

      const data = await response.json();

      alert(data.message);

      if (data.success) {

        setRecipient("");
        setAccount("");
        setIfsc("");
        setAmount("");
        setRemarks("");

      }

    } catch (err) {

      console.error(err);

      alert("Server Error");

    }

  };

  return (

    <MainLayout>

      <div className="bank-card">

        <h2>💸 Transfer Money</h2>

        <input
          className="bank-input"
          type="text"
          placeholder="Recipient Name"
          value={recipient}
          onChange={(e) => setRecipient(e.target.value)}
        />

        <input
          className="bank-input"
          type="text"
          placeholder="Account Number"
          value={account}
          onChange={(e) => setAccount(e.target.value)}
        />

        <input
          className="bank-input"
          type="text"
          placeholder="IFSC Code"
          value={ifsc}
          onChange={(e) => setIfsc(e.target.value)}
        />

        <input
          className="bank-input"
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />

        <textarea
          className="bank-input"
          rows="4"
          placeholder="Remarks"
          value={remarks}
          onChange={(e) => setRemarks(e.target.value)}
        />

        <button
          className="bank-btn"
          onClick={handleTransfer}
        >
          Transfer Money
        </button>

      </div>

    </MainLayout>

  );

}

export default Transfer;