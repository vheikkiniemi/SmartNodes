import express from "express";
import pool from "../db/pool.js";

const router = express.Router();

// GET /api/devices
router.get("/", async (req, res) => {
	try {
		const { rows } = await pool.query(
			"SELECT * FROM devices",
		);

		return res.status(200).json({ ok: true, data: rows });
	} catch (err) {
		console.error("READ ALL failed:", err);
		return res.status(500).json({ ok: false, error: "Database error" });
	}
});

// TODO!
// GET /api/devices/:id
router.get("/:id", async (req, res) => {
	const id = parseInt(req.params.id, 10)

	if (isNaN(id)) {
		return res.status(400).json({ ok: false, error: "Invalid ID" });
	}

	try {
		const { rows } = await pool.query(
			"SELECT * FROM devices WHERE id = $1",
			[id],
		);

		if (rows.length === 0) {
			return res
				.status(404)
				.json({ ok: false, error: "Device not found" });
		}

		return res.status(200).json({ ok: true, data: rows[0] });
	} catch (err) {
		console.error("READ ONE failed:", err);
		return res.status(500).json({ ok: false, error: "Database error" });
	}
});

export default router;
