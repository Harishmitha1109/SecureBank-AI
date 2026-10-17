import "../styles/Dashboard.css";
import { Link } from "react-router-dom";
import MainLayout from "../layout/MainLayout";
import { useEffect, useState, useRef } from "react";

function Dashboard() {

  const user = JSON.parse(localStorage.getItem("user"));

  // ==========================================
  // State
  // ==========================================

  const [balance, setBalance] = useState(0);

  const [transactions, setTransactions] = useState([]);

  const [aiResult, setAiResult] = useState({
    prediction: "Analyzing...",
    confidence: 0,
    risk: "CHECKING"
  });

  // ==========================================
  // HIGH RISK COUNTER
  // ==========================================

  const highRiskCount = useRef(0);

  const REQUIRED_HIGH_CHECKS = 3;


  // ==========================================
  // Get Current Balance
  // ==========================================

  useEffect(() => {

    if (!user?.email) return;

    const getBalance = async () => {

      try {

        const response = await fetch(
          `http://127.0.0.1:5000/balance/${user.email}`
        );

        const data = await response.json();

        setBalance(
          Number(data.balance) || 0
        );

      } catch (error) {

        console.error(
          "Balance Error:",
          error
        );

      }

    };

    getBalance();

    const interval = setInterval(
      getBalance,
      5000
    );

    return () => clearInterval(interval);

  }, [user?.email]);


  // ==========================================
  // Get Transactions
  // ==========================================

  useEffect(() => {

    if (!user?.email) return;

    const getTransactions = async () => {

      try {

        const response = await fetch(
          `http://127.0.0.1:5000/transactions/${user.email}`
        );

        const data = await response.json();

        setTransactions(
          Array.isArray(data) ? data : []
        );

      } catch (error) {

        console.error(
          "Transaction Error:",
          error
        );

      }

    };

    getTransactions();

    const interval = setInterval(
      getTransactions,
      5000
    );

    return () => clearInterval(interval);

  }, [user?.email]);


  // ==========================================
  // AI BEHAVIORAL PREDICTION
  // ==========================================

  useEffect(() => {

    if (!user?.email) return;

    let isChecking = false;

    const checkBehavior = async () => {

      // Prevent overlapping AI requests
      if (isChecking) return;

      isChecking = true;

      try {

        const response = await fetch(
          "http://127.0.0.1:5000/predict-behavior",
          {
            method: "POST",

            headers: {
              "Content-Type": "application/json"
            },

            body: JSON.stringify({
              email: user.email
            })
          }
        );

        const data = await response.json();


        if (data.success) {

          // ==========================================
          // HIGH RISK CONFIRMATION
          // ==========================================

          if (
            data.risk === "HIGH" &&
            data.prediction === "Suspicious User"
          ) {

            highRiskCount.current += 1;

            console.log(
              `HIGH risk confirmation: ${highRiskCount.current}/${REQUIRED_HIGH_CHECKS}`
            );

          } else {

            // Reset counter if behavior becomes
            // normal again.

            highRiskCount.current = 0;

          }


          // ==========================================
          // LOGOUT ONLY AFTER 3 CONSECUTIVE HIGH
          // ==========================================

          if (
            highRiskCount.current >=
            REQUIRED_HIGH_CHECKS
          ) {

            alert(
              "🚨 Suspicious activity detected.\n\n" +
              "Your behavioral pattern does not match " +
              "your registered profile.\n\n" +
              "For your security, your session has been terminated."
            );

            localStorage.removeItem("user");

            window.location.href = "/login";

            return;
          }


          // ==========================================
          // SHOW CURRENT AI RESULT
          // ==========================================

          setAiResult({

            prediction:
              data.prediction,

            confidence:
              data.confidence,

            risk:
              data.risk

          });

        } else {

          console.log(
            "AI:",
            data.message
          );

        }

      } catch (error) {

        console.error(
          "AI Prediction Error:",
          error
        );

      } finally {

        isChecking = false;

      }

    };


    // ==========================================
    // Initial AI Check
    // ==========================================

    checkBehavior();


    // ==========================================
    // Check AI Every 10 Seconds
    // ==========================================

    const interval = setInterval(
      checkBehavior,
      10000
    );


    return () => clearInterval(
      interval
    );

  }, [user?.email]);


  // ==========================================
  // AI STATUS
  // ==========================================

  const isGenuine =
    aiResult.prediction === "Genuine User";


  const isAnalyzing =
    aiResult.prediction === "Analyzing...";


  // ==========================================
  // RISK CSS CLASS
  // ==========================================

  let riskClass = "green";


  if (aiResult.risk === "MEDIUM") {

    riskClass = "orange";

  }


  if (aiResult.risk === "HIGH") {

    riskClass = "red";

  }


  // ==========================================
  // RENDER
  // ==========================================

  return (

    <MainLayout>

      {/* =====================================
          Welcome Card
      ====================================== */}

      <div className="welcome-card">

        <div>

          <h1>
            👋 Good Afternoon, {user?.name}
          </h1>

          <p>
            Welcome back to SecureBank AI
          </p>

        </div>

        <div className="notify">

          🔔

        </div>

      </div>


      {/* =====================================
          Balance Card
      ====================================== */}

      <div className="balance-card">

        <h3>
          Current Balance
        </h3>

        <h1>
          ₹{Number(balance).toLocaleString("en-IN")}
        </h1>

      </div>


      {/* =====================================
          Statistics
      ====================================== */}

      <div className="stats">

        <div className="stat-card">

          <h4>
            Total Credit
          </h4>

          <h2>

            ₹
            {transactions
              .filter(
                (t) => t.type === "Credit"
              )
              .reduce(
                (total, t) =>
                  total +
                  Number(t.amount || 0),
                0
              )
              .toLocaleString("en-IN")}

          </h2>

        </div>


        <div className="stat-card">

          <h4>
            Total Debit
          </h4>

          <h2>

            ₹
            {transactions
              .filter(
                (t) => t.type === "Debit"
              )
              .reduce(
                (total, t) =>
                  total +
                  Number(t.amount || 0),
                0
              )
              .toLocaleString("en-IN")}

          </h2>

        </div>


        <div className="stat-card">

          <h4>
            Transactions
          </h4>

          <h2>
            {transactions.length}
          </h2>

        </div>

      </div>


      {/* =====================================
          Quick Actions
      ====================================== */}

      <h3 className="section-title">

        Quick Actions

      </h3>


      <div className="actions">

        <Link
          to="/transfer"
          className="action-card"
        >

          💸

          <p>
            Transfer
          </p>

        </Link>


        <Link
          to="/transactions"
          className="action-card"
        >

          📜

          <p>
            History
          </p>

        </Link>


        <Link
          to="/cards"
          className="action-card"
        >

          💳

          <p>
            Cards
          </p>

        </Link>


        <Link
          to="/profile"
          className="action-card"
        >

          👤

          <p>
            Profile
          </p>

        </Link>

      </div>


      {/* =====================================
          Recent Transactions
      ====================================== */}

      <div className="recent-card">

        <h3>
          Recent Transactions
        </h3>


        <table>

          <tbody>

            {transactions.length === 0 ? (

              <tr>

                <td colSpan="2">

                  No Transactions Yet

                </td>

              </tr>

            ) : (

              transactions
                .slice(-3)
                .reverse()
                .map((t, index) => (

                  <tr key={index}>

                    <td>

                      {t.type === "Credit"
                        ? "Deposit"
                        : t.recipient}

                    </td>


                    <td
                      className={
                        t.type === "Credit"
                          ? "credit"
                          : "debit"
                      }
                    >

                      {t.type === "Credit"
                        ? "+ "
                        : "- "}

                      ₹
                      {Number(
                        t.amount || 0
                      ).toLocaleString(
                        "en-IN"
                      )}

                    </td>

                  </tr>

                ))

            )}

          </tbody>

        </table>

      </div>


      {/* =====================================
          AI SECURITY CARD
      ====================================== */}

      <div className="ai-card">

        <h2>
          🤖 AI Security
        </h2>


        <div className="verified">

          {isAnalyzing ? (

            <>
              🟡 Analyzing Behavior...
            </>

          ) : isGenuine ? (

            <>
              🟢 Genuine User
            </>

          ) : (

            <>
              🔴 Suspicious User
            </>

          )}

        </div>


        <div className="ai-grid">

          <div>

            <p>
              Confidence
            </p>

            <h3>
              {aiResult.confidence}%
            </h3>

          </div>


          <div>

            <p>
              Risk
            </p>

            <h3
              className={riskClass}
            >

              {aiResult.risk}

            </h3>

          </div>


          <div>

            <p>
              Model
            </p>

            <h3>
              Behavioral AI
            </h3>

          </div>


          <div>

            <p>
              Behavior
            </p>

            <h3>

              {isAnalyzing
                ? "..."
                : isGenuine
                ? "✓"
                : "⚠"}

            </h3>

          </div>

        </div>


        <p className="ai-description">

          Behavioral biometrics continuously analyze
          mouse, click, scroll, and session patterns.

        </p>


      </div>


    </MainLayout>

  );

}


export default Dashboard;