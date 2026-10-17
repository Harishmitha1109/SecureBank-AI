import { useEffect, useState } from "react";
import MainLayout from "../layout/MainLayout";
import "../styles/Banking.css";

function Transactions() {

  const user = JSON.parse(localStorage.getItem("user"));

  const [transactions, setTransactions] = useState([]);

  useEffect(() => {

    fetch(`http://127.0.0.1:5000/transactions/${user.email}`)
      .then((res) => res.json())
      .then((data) => setTransactions(data))
      .catch((err) => console.log(err));

  }, []);

  return (

    <MainLayout>

      <div className="bank-card">

        <h2>📜 Transaction History</h2>

        <table className="transaction-table">

          <thead>

            <tr>

              <th>Recipient</th>

              <th>Account</th>

              <th>IFSC</th>

              <th>Amount</th>

              <th>Remarks</th>

            </tr>

          </thead>

          <tbody>

            {transactions.length === 0 ? (

              <tr>

                <td colSpan="5">
                  No Transactions Found
                </td>

              </tr>

            ) : (

              transactions.map((t, index) => (

                <tr key={index}>

                  <td>{t.recipient}</td>

                  <td>{t.account}</td>

                  <td>{t.ifsc}</td>

                  <td>₹ {t.amount}</td>

                  <td>{t.remarks}</td>

                </tr>

              ))

            )}

          </tbody>

        </table>

      </div>

    </MainLayout>

  );

}

export default Transactions;