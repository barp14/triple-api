import axios from 'axios'

const EMAIL_API_URL = "http://localhost:5001/disparar-email"

class GenerateArchiveController {
  async handle (req, res) {
    const response = await axios.get(`${EMAIL_API_URL}`);
    
    return res.json(response)
  }
}

export { GenerateArchiveController }