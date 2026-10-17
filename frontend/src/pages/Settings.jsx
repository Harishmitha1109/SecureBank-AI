import { useState } from "react";
import MainLayout from "../layout/MainLayout";
import "../styles/Banking.css";

function Settings() {

  const [settings, setSettings] = useState({

    emailAlerts: true,
    smsAlerts: true,
    behavioralAuth: true,
    continuousMonitoring: true,
    rememberDevice: false,

  });

  const handleChange = (e) => {

    setSettings({
      ...settings,
      [e.target.name]: e.target.checked,
    });

  };

  const handleSave = () => {

    alert("Settings Saved Successfully");

  };

  return (

    <MainLayout>

      <div className="bank-card">

        <h2>⚙️ Settings</h2>

        <div className="setting-item">

          <label>Email Notifications</label>

          <input
            type="checkbox"
            name="emailAlerts"
            checked={settings.emailAlerts}
            onChange={handleChange}
          />

        </div>

        <div className="setting-item">

          <label>SMS Notifications</label>

          <input
            type="checkbox"
            name="smsAlerts"
            checked={settings.smsAlerts}
            onChange={handleChange}
          />

        </div>

        <div className="setting-item">

          <label>Behavioral Authentication</label>

          <input
            type="checkbox"
            name="behavioralAuth"
            checked={settings.behavioralAuth}
            onChange={handleChange}
          />

        </div>

        <div className="setting-item">

          <label>Continuous Monitoring</label>

          <input
            type="checkbox"
            name="continuousMonitoring"
            checked={settings.continuousMonitoring}
            onChange={handleChange}
          />

        </div>

        <div className="setting-item">

          <label>Remember This Device</label>

          <input
            type="checkbox"
            name="rememberDevice"
            checked={settings.rememberDevice}
            onChange={handleChange}
          />

        </div>

        <button
          className="bank-btn"
          onClick={handleSave}
        >
          Save Settings
        </button>

      </div>

    </MainLayout>

  );

}

export default Settings;
