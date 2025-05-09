import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Tabs, Tab, Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Container, Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button } from '@mui/material';

function Dashboard() {
  const [value, setValue] = useState(0);  // Controle das tabs
  const [clientes, setClientes] = useState([]);
  const [campanhas, setCampanhas] = useState([]);
  
  // Para os modais de adicionar
  const [openCliente, setOpenCliente] = useState(false);
  const [openCampanha, setOpenCampanha] = useState(false);

  // Estados para os dados de clientes e campanhas
  const [novoCliente, setNovoCliente] = useState({ nome: '', email: '' });
  const [novaCampanha, setNovaCampanha] = useState({ nome: '', tag: '' });

  // Estado para "Envio de Campanha"
  const [campanhaTag, setCampanhaTag] = useState('');
  const [envioStatus, setEnvioStatus] = useState('');

  // Função para alternar entre as tabs
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  // Função para buscar clientes
  const buscarClientes = async () => {
    try {
      const response = await axios.get('http://localhost:3000/clientes');
      setClientes(response.data);
    } catch (error) {
      console.error("Erro ao buscar clientes:", error);
    }
  };

  // Função para buscar campanhas
  const buscarCampanhas = async () => {
    try {
      const response = await axios.get('http://localhost:3000/campanhas');
      setCampanhas(response.data);
    } catch (error) {
      console.error("Erro ao buscar campanhas:", error);
    }
  };

  // Função para criar cliente
  const criarCliente = async () => {
    try {
      await axios.post('http://localhost:3000/clientes', novoCliente);
      setNovoCliente({ nome: '', email: '' });
      setOpenCliente(false);
      buscarClientes();  // Atualiza a lista de clientes
    } catch (error) {
      console.error("Erro ao criar cliente:", error);
    }
  };

  // Função para criar campanha
  const criarCampanha = async () => {
    try {
      await axios.post('http://localhost:3000/campanhas', novaCampanha);
      setNovaCampanha({ nome: '', tag: '' });
      setOpenCampanha(false);
      buscarCampanhas();  // Atualiza a lista de campanhas
    } catch (error) {
      console.error("Erro ao criar campanha:", error);
    }
  };
  
  const dispararEmailByTag = async () => {
    try {
      setEnvioStatus('Enviando...');
      
      const response = await axios.post(`http://localhost:5000/disparar-email-by-tag?campanhatag=${campanhaTag}`);
      
      if (response.status === 200) {
        setEnvioStatus('Envio realizado com sucesso!');
      } else {
        setEnvioStatus('Erro ao disparar e-mail.');
      }
    } catch (error) {
      console.error("Erro ao disparar e-mail:", error);
      setEnvioStatus('Erro ao disparar e-mail.');
    }
  };

const generateArchive = async () => {
  try {
    const response = await axios.get('http://localhost:4000/generate-archive', {
      responseType: 'blob',  // Garantindo que a resposta seja tratada como 'blob' (arquivo binário)
    });

    // Criar uma URL temporária para o arquivo
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'planilha.xlsx');  // Nome do arquivo para download
    document.body.appendChild(link);
    link.click();  // Simula o clique para iniciar o download
    link.parentNode.removeChild(link);  // Remove o link temporário após o download

    // Liberar o objeto URL após o uso
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Erro ao gerar o arquivo:', error);
  }
};

  // Chama as funções dependendo da tab ativa
  useEffect(() => {
    if (value === 0) {
      buscarClientes();  // Carrega clientes na tab "Clientes"
    } else if (value === 1) {
      buscarCampanhas();  // Carrega campanhas na tab "Campanhas"
    }
  }, [value]);

  return (
    <div>
      <Container maxWidth="lg" sx={{ textAlign: 'center', paddingTop: '20px' }}>
        <h1>Sistema de Prospecção de Leads</h1>

        {/* Tab Layout */}
        <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
          <Tabs value={value} onChange={handleChange} aria-label="tabs de navegação" centered>
            <Tab label="Clientes" />
            <Tab label="Campanhas" />
            <Tab label="Envio de Campanhas" />
          </Tabs>
        </Box>

        {/* Conteúdo da Tab "Clientes" */}
        {value === 0 && (
          <Box>
            <Button variant="contained" color="primary" onClick={() => setOpenCliente(true)}>
              Adicionar Cliente
            </Button>
            <TableContainer component={Paper} variant="outlined" sx={{ marginTop: '20px' }}>
              <Table aria-label="clientes table">
                <TableHead>
                  <TableRow>
                    <TableCell>Nome do Cliente</TableCell>
                    <TableCell>Email do Cliente</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {clientes.length > 0 ? (
                    clientes.map((cliente) => (
                      <TableRow key={cliente.email}>
                        <TableCell>{cliente.nome}</TableCell>
                        <TableCell>{cliente.email}</TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={2}>Não há clientes cadastrados.</TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {/* Conteúdo da Tab "Campanhas" */}
        {value === 1 && (
          <Box>
            <Button variant="contained" color="primary" onClick={() => setOpenCampanha(true)}>
              Adicionar Campanha
            </Button>
            <TableContainer component={Paper} variant="outlined" sx={{ marginTop: '20px' }}>
              <Table aria-label="campanhas table">
                <TableHead>
                  <TableRow>
                    <TableCell>Nome da Campanha</TableCell>
                    <TableCell>Tag da Campanha</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {campanhas.length > 0 ? (
                    campanhas.map((campanha) => (
                      <TableRow key={campanha.nome}>
                        <TableCell>{campanha.nome}</TableCell>
                        <TableCell>{campanha.tag}</TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={2}>Não há campanhas cadastradas.</TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {/* Conteúdo da Tab "Envio de Campanhas" */}
        {value === 2 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Enviar Campanha
            </Typography>
            <TextField
              label="Tag da Campanha"
              fullWidth
              value={campanhaTag}
              onChange={(e) => setCampanhaTag(e.target.value)}
              sx={{ marginBottom: 2 }}
            />
            <div className='buttons-container'> 
              <Button variant="contained" color="primary" onClick={dispararEmailByTag}>
                Enviar E-mails
              </Button>
              {envioStatus && (
                <Typography variant="body2" color="textSecondary" sx={{ marginTop: 2 }}>
                  {envioStatus}
                </Typography>
              )}
              <Button variant="outlined" color="primary" onClick={generateArchive}>
                Gerar Arquivo
              </Button>
            </div>
          </Box>
        )}

        {/* Modal para Adicionar Cliente */}
        <Dialog open={openCliente} onClose={() => setOpenCliente(false)}>
          <DialogTitle>Adicionar Cliente</DialogTitle>
          <DialogContent>
            <TextField
              label="Nome do Cliente"
              fullWidth
              value={novoCliente.nome}
              onChange={(e) => setNovoCliente({ ...novoCliente, nome: e.target.value })}
              sx={{ marginBottom: 2 }}
            />
            <TextField
              label="Email do Cliente"
              fullWidth
              value={novoCliente.email}
              onChange={(e) => setNovoCliente({ ...novoCliente, email: e.target.value })}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenCliente(false)} color="primary">Cancelar</Button>
            <Button onClick={criarCliente} color="primary">Adicionar</Button>
          </DialogActions>
        </Dialog>

        {/* Modal para Adicionar Campanha */}
        <Dialog open={openCampanha} onClose={() => setOpenCampanha(false)}>
          <DialogTitle>Adicionar Campanha</DialogTitle>
          <DialogContent>
            <TextField
              label="Nome da Campanha"
              fullWidth
              value={novaCampanha.nome}
              onChange={(e) => setNovaCampanha({ ...novaCampanha, nome: e.target.value })}
              sx={{ marginBottom: 2 }}
            />
            <TextField
              label="Tag da Campanha"
              fullWidth
              value={novaCampanha.tag}
              onChange={(e) => setNovaCampanha({ ...novaCampanha, tag: e.target.value })}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenCampanha(false)} color="primary">Cancelar</Button>
            <Button onClick={criarCampanha} color="primary">Adicionar</Button>
          </DialogActions>
        </Dialog>
      </Container>
    </div>
  );
}

export default Dashboard;
