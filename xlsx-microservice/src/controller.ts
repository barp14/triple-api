import axios from 'axios';
import { redisClient } from './redis.js';
import { Request, Response } from 'express';
import * as XLSX from 'xlsx';

const EMAIL_API_URL =  process.env.EMAIL_API_URL; //'http://localhost:5000/disparar-email'; 
const CACHE_KEY = 'e-mail--cache';
const CACHE_EXP = 60 * 1000; // 1 minute

interface EmailData {
  campanha: string;
  email: string;
  mensagem: string;
  status: 'enviado' | 'pendente';
}

class GenerateArchiveController {
  public handle = async (req: Request, res: Response): Promise<void> => {
    try {
      const cache = await redisClient.get(CACHE_KEY);
      let data: EmailData[] = [];

      if (cache) {
        console.log('-----> Hit Cache');
        data = JSON.parse(cache);
      } else {
        console.log('>> EMAIL_API_URL raw:', EMAIL_API_URL);
        console.log('-----> Miss Cache');
        const response = await axios.post(`${EMAIL_API_URL}`);
        data = response.data as EmailData[];
        await redisClient.set(CACHE_KEY, JSON.stringify(data), { PX: CACHE_EXP });
      }
  
      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Planilha');
  
      const xlsxBuffer = XLSX.write(wb, { type: 'buffer', bookType: 'xlsx'});
      const fileName = `planilha_${new Date().toISOString().replace(/[:]/g, '-')}.xlsx`;
      
      res
        .setHeader('Content-Disposition', `attachment; filename=${fileName}`)
        .setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        .setHeader('Content-Length', xlsxBuffer.length);

      res.end(xlsxBuffer);
    } catch (err: any) {
      console.error('Erro ao chamar API de e-mail:', err.code, err.message, err.response?.status);
      res.status(500).json({ error: 'Erro ao realizar a requisição' });
    }
    
  }
}

export { GenerateArchiveController }