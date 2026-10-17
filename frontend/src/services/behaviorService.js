const API_URL = "http://127.0.0.1:5000/behavior";

export async function saveBehaviorSession(sessionData) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sessionData),
    });

    return await response.json();
  } catch (error) {
    console.error("Error saving behavior:", error);
    return null;
  }
}