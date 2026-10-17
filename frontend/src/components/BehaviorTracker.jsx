import { useEffect, useRef } from "react";

function BehaviorTracker({ email }) {

  const mouseDistance = useRef(0);
  const clicks = useRef(0);
  const scrollDistance = useRef(0);
  const sessionStart = useRef(Date.now());

  const lastX = useRef(null);
  const lastY = useRef(null);

  useEffect(() => {

    const device =
      /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent)
        ? "Mobile"
        : "Desktop";

    const handleMouseMove = (e) => {

      if (lastX.current !== null) {

        const dx = e.clientX - lastX.current;
        const dy = e.clientY - lastY.current;

        mouseDistance.current += Math.sqrt(dx * dx + dy * dy);
      }

      lastX.current = e.clientX;
      lastY.current = e.clientY;

    };

    const handleClick = () => {

      clicks.current++;

    };

    const handleScroll = () => {

      scrollDistance.current = window.scrollY;

    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("click", handleClick);
    window.addEventListener("scroll", handleScroll);

    const timer = setInterval(async () => {

      const sessionDuration =
        Math.floor((Date.now() - sessionStart.current) / 1000);

      try {

        await fetch("http://127.0.0.1:5000/behavior", {

          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            email,
            device,
            mouse_distance: Math.round(mouseDistance.current),
            clicks: clicks.current,
            scroll_distance: scrollDistance.current,
            session_duration: sessionDuration,
            timestamp: new Date().toISOString()

          })

        });

      } catch (err) {
        console.error(err);
      }

    }, 5000);

    return () => {

      clearInterval(timer);

      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("click", handleClick);
      window.removeEventListener("scroll", handleScroll);

    };

  }, [email]);

  return null;

}

export default BehaviorTracker;