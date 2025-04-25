import express from 'express';
import cors from 'cors';
import { GenerateArchiveController } from './controller.js'

const HOST = 4000

const app = express()
app.use(cors())

app.post('/generate-archive', new GenerateArchiveController().handle)

app.listen(HOST, () => console.log(`Servidor rodando na porta ${HOST}`))