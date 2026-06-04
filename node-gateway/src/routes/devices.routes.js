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

// GET /api/devices/:device_uid
router.get("/:device_uid", async (req, res) => {
    const device_uid = req.params.device_uid;

    try {
        const { rows } = await pool.query(
            `
            SELECT *
            FROM devices
            WHERE device_uid = $1
            `,
            [device_uid]
        );

        if (rows.length === 0) {
            return res
                .status(404)
                .json({ ok: false, error: "Device not found" });
        }

        return res.status(200).json({
            ok: true,
            data: rows[0]
        });

    } catch (err) {
        console.error("READ DEVICE failed:", err);

        return res.status(500).json({
            ok: false,
            error: "Database error"
        });
    }
});

export default router;
