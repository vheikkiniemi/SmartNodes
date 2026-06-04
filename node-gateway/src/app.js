import express from "express";
import devicesRouter from "./routes/devices.routes.js";
import messagesRouter from "./routes/messages.routes.js";

const app = express();
app.use(express.json());

app.use("/api/devices", devicesRouter);
app.use("/api/messages", messagesRouter);

app.use("/api", (req, res) => {
	return res.status(404).json({
		ok: false,
		error: "Not found",
		path: req.originalUrl,
	});
});

// ----------------------------
// Frontend 404 (unknown pages)
// ----------------------------
app.use((req, res) => {
  // If you have a dedicated 404.html, prefer that.
  // Otherwise return a simple message.
  return res.status(404).send("404 - Page not found");
});

app.use((err, req, res, next) => {
	console.error("Unhandled error:", err);

	if (res.headersSent) return next(err);

	return res.status(500).json({
		ok: false,
		error: "Internal server error",
	});
});

export default app;
