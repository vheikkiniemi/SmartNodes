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

app.use((err, req, res, next) => {
	console.error("Unhandled error:", err);

	if (res.headersSent) return next(err);

	return res.status(500).json({
		ok: false,
		error: "Internal server error",
	});
});

export default app;
