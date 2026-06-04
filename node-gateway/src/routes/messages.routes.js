import express from "express";
import pool from "../db/pool.js";

const router = express.Router();

// TODO: From date, payload search, relation info
// GET /api/messages
router.get("/", async (req, res) => {
    const topic = req.query.topic || null
	try {
		const { rows } = await pool.query(
			"SELECT * FROM messages WHERE ($1::text is null or topic = $1)",
            [topic]
		);

		return res.status(200).json({ ok: true, data: rows });
	} catch (err) {
		console.error("READ ALL failed:", err);
		return res.status(500).json({ ok: false, error: "Database error" });
	}
});

// GET /api/messages/device/:device_uid
router.get("/device/:device_uid", async (req, res) => {
    const device_uid = req.params.device_uid;

    try {
        const { rows } = await pool.query(
            `
            SELECT *
            FROM messages
            WHERE device_uid = $1
            ORDER BY recorded_at DESC
            `,
            [device_uid]
        );

        return res.status(200).json({ ok: true, data: rows });
    } catch (err) {
        console.error("READ BY DEVICE UID failed:", err);
        return res.status(500).json({ ok: false, error: "Database error" });
    }
});

export default router;
