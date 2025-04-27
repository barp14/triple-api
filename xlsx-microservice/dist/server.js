import express from 'express';
import cors from 'cors';
import { router } from './routes.js';
const app = express();
const HOST = 4000;
app.use(express.json());
app.use(router);
app.use(cors());
app.use((err, req, res, next) => {
    if (err instanceof Error) {
        res.status(400).json({
            error: err.message
        });
    }
    res.status(500).json({
        status: 'error',
        message: 'Internal server error.'
    });
});
app.listen(HOST, () => {
    console.log(`Servidor rodando na porta ${HOST}`);
});
