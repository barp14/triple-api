import axios from 'axios';
import { redisClient } from './redis.js';
import * as XLSX from 'xlsx';
const EMAIL_API_URL = "http://localhost:5001/disparar-email";
const CACHE_KEY = 'e-mail--cache';
const CACHE_EXP = 60 * 1000;
class GenerateArchiveController {
    constructor() {
        this.handle = async (req, res) => {
            try {
                const cache = await redisClient.get(CACHE_KEY);
                let data = [];
                if (cache) {
                    console.log('-----> Hit Cache');
                    data = JSON.parse(cache);
                }
                else {
                    console.log('-----> Miss Cache');
                    const response = await axios.post(`${EMAIL_API_URL}`);
                    data = response.data;
                    await redisClient.set(CACHE_KEY, JSON.stringify(data), { PX: CACHE_EXP });
                }
                const ws = XLSX.utils.json_to_sheet(data);
                const wb = XLSX.utils.book_new();
                XLSX.utils.book_append_sheet(wb, ws, 'Planilha');
                const xlsxBuffer = XLSX.write(wb, { type: 'buffer', bookType: 'xlsx' });
                const fileName = `planilha_${new Date().toISOString().replace(/[:]/g, '-')}.xlsx`;
                res
                    .setHeader('Content-Disposition', `attachment; filename=${fileName}`)
                    .setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    .setHeader('Content-Length', xlsxBuffer.length);
                res.end(xlsxBuffer);
            }
            catch (error) {
                res.status(500).json({ error: 'Erro ao realizar a requisição' });
            }
        };
    }
}
export { GenerateArchiveController };
