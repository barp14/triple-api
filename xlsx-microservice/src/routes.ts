import { Router } from 'express';
import { GenerateArchiveController } from './controller.js';

const router = Router();

router.get('/generate-archive', new GenerateArchiveController().handle);

export { router };