// Import your JSON data
import sampleData from "./new_results.json";

// App.js
import React, { useState, useMemo } from "react";
import {
  Box,
  Typography,
  Modal,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
  OutlinedInput,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
} from "@mui/material";

// Import MUI icons for GitHub and ArXiv
import GitHubIcon from "@mui/icons-material/GitHub";
import ArticleIcon from "@mui/icons-material/Article";

// Import Chart components
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


// Company colors constant
const COMPANY_COLORS = {
  openai: "#74AA9C",      // OpenAI green
  "meta-llama": "#044EAB",// Meta blue
  anthropic: "#D4C5B9",   // Anthropic beige
  google: "#669DF7",      // Google blue
  "x-ai": "#000000",      // X black
  mistralai: "#F54E42"    // Mistral red
};

// Modal styling
const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "80%",
  maxHeight: "80vh",
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
  overflowY: "auto",
};

function App() {
  // Extract unique questions from the data
  const uniqueQuestions = useMemo(() => {
    const questionsSet = new Set();
    Object.values(sampleData.models).forEach((model) => {
      Object.values(model).forEach((paramObj) => {
        Object.keys(paramObj).forEach((question) => {
          questionsSet.add(question);
        });
      });
    });
    return Array.from(questionsSet);
  }, []);

  // State for selected questions filter
  const [selectedQuestions, setSelectedQuestions] = useState([]);
  // State for model detail modal
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedModelName, setSelectedModelName] = useState(null);

  // Handle filter change
  const handleFilterChange = (event) => {
    setSelectedQuestions(event.target.value);
  };

  // "Select All Questions" button handler
  const handleSelectAll = () => {
    setSelectedQuestions(uniqueQuestions);
  };

  // "Deselect All Questions" button handler
  const handleDeselectAll = () => {
    setSelectedQuestions([]);
  };

  // Compute aggregated metrics for each model based on the filter,
  // summing the coherence and dissimilarity scores.
  // Total coherence is rounded to the nearest whole number,
  // and total dissimilarity to the nearest tenth.
  const modelsMetrics = useMemo(() => {
    const metrics = [];
    for (const [modelName, params] of Object.entries(sampleData.models)) {
      let totalResponses = 0;
      let sumCoherence = 0;
      let sumDissimilarity = 0;
      // Keep filtered data for drill-down
      let filteredData = {};

      for (const [paramKey, questions] of Object.entries(params)) {
        for (const [question, responses] of Object.entries(questions)) {
          // Include only matching questions or all if none selected
          if (
            selectedQuestions.length === 0 ||
            selectedQuestions.includes(question)
          ) {
            if (!filteredData[paramKey]) {
              filteredData[paramKey] = {};
            }
            filteredData[paramKey][question] = responses;

            responses.forEach((resp) => {
              totalResponses++;
              sumCoherence += resp.coherence_score;
              sumDissimilarity += resp.embedding_dissimilarity_score;
            });
          }
        }
      }
      const totalCoherenceStr =
        totalResponses > 0 ? Math.round(sumCoherence).toString() : "0";
      const totalDissimilarityStr =
        totalResponses > 0 ? parseFloat(sumDissimilarity.toFixed(1)).toString() : "0";

      metrics.push({
        modelName,
        totalResponses,
        totalCoherence: totalCoherenceStr,
        totalDissimilarity: totalDissimilarityStr,
        filteredData, // Save for the drill-down view
      });
    }
    return metrics.sort((a, b) => b.totalResponses - a.totalResponses);
  }, [selectedQuestions]);

  // Compute the best (highest) total score for scaling the horizontal bar
  const bestTotal = modelsMetrics.length > 0 ? modelsMetrics[0].totalResponses : 0;

  // Open model detail modal
  const handleModelClick = (modelName) => {
    setSelectedModelName(modelName);
    setModalOpen(true);
  };

  // Close modal
  const handleClose = () => {
    setModalOpen(false);
    setSelectedModelName(null);
  };

  // Get detailed data for selected model
  const selectedModelDetail = useMemo(() => {
    if (!selectedModelName) return null;
    const model = modelsMetrics.find((m) => m.modelName === selectedModelName);
    return model?.filteredData || null;
  }, [selectedModelName, modelsMetrics]);

  return (
    <Box sx={{ p: 4 }}>
      {/* Intro Header */}
      <Typography variant="h4" align="center" sx={{ fontWeight: "bold", fontSize: "2rem", mb: 1 }}>
        AidanBench: Stress-Testing Language Model Creativity on Open-Ended Questions
      </Typography>
      
      {/* Authors */}
      <Box sx={{ display: "flex", justifyContent: "center", flexWrap: "wrap", gap: 2, mb: 1 }}>
        <Box sx={{ textAlign: "center" }}>
          <a
            href="https://aidanmclaughlin.notion.site/Aidan-McLaughlin-13424dff9b2a80608c5eec52ac79207d"
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <Typography
              sx={{
                fontWeight: "bold",
                transition: "transform 0.2s",
                "&:hover": { transform: "translateY(-2px)" },
              }}
            >
              Aidan McLaughlin*<sup>1</sup>
            </Typography>
          </a>
        </Box>
        <Box sx={{ textAlign: "center" }}>
          <a
            href="https://jamescampbell.me"
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <Typography
              sx={{
                fontWeight: "bold",
                transition: "transform 0.2s",
                "&:hover": { transform: "translateY(-2px)" },
              }}
            >
              James Campbell*<sup>2</sup>
            </Typography>
          </a>
        </Box>
        <Box sx={{ textAlign: "center" }}>
          <a
            href="https://www.linkedin.com/in/anujau/"
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <Typography
              sx={{
                fontWeight: "bold",
                transition: "transform 0.2s",
                "&:hover": { transform: "translateY(-2px)" },
              }}
            >
              Anuja Uppuluri*<sup>2</sup>
            </Typography>
          </a>
        </Box>
        <Box sx={{ textAlign: "center" }}>
          <a
            href="https://www.cs.cmu.edu/~./yiming/"
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <Typography
              sx={{
                fontWeight: "bold",
                transition: "transform 0.2s",
                "&:hover": { transform: "translateY(-2px)" },
              }}
            >
              Yiming Yang<sup>2</sup>
            </Typography>
          </a>
        </Box>
      </Box>
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Typography variant="caption" display="block">
          <sup>1</sup> OpenAI (Work done while at Topology Research Corporation)
        </Typography>
        <Typography variant="caption" display="block">
          <sup>2</sup> Carnegie Mellon University
        </Typography>
      </Box>

      {/* Intro Paragraph */}
      <Typography variant="body1" align="center" sx={{ mb: 2 }}>
      Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder 
      </Typography>

      {/* External Links for GitHub and ArXiv */}
      <Box sx={{ display: "flex", justifyContent: "center", gap: 2, mb: 4 }}>
        <IconButton
          component="a"
          href="https://github.com/aidanmclaughlin/AidanBench"
          target="_blank"
          rel="noopener noreferrer"
        >
          <GitHubIcon fontSize="large" />
        </IconButton>
        <IconButton
          component="a"
          href="https://arxiv.org/abs/2310.01405"
          target="_blank"
          rel="noopener noreferrer"
        >
          <ArticleIcon fontSize="large" />
        </IconButton>
      </Box>

      {/* Filter controls with Select/Deselect All buttons */}
      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          gap: 2,
          alignItems: "center",
          justifyContent: "center",
          mb: 4,
        }}
      >
        <FormControl sx={{ minWidth: 300 }}>
          <InputLabel id="question-filter-label" sx={{ fontWeight: "bold" }}>
            Filter by Question
          </InputLabel>
          <Select
            labelId="question-filter-label"
            multiple
            value={selectedQuestions}
            onChange={handleFilterChange}
            input={<OutlinedInput label="Filter by Question" />}
            renderValue={(selected) => selected.join(", ")}
            sx={{ fontWeight: "bold", fontSize: "1rem" }}
          >
            {uniqueQuestions.map((question) => (
              <MenuItem key={question} value={question}>
                <Checkbox checked={selectedQuestions.indexOf(question) > -1} />
                <ListItemText primary={question} sx={{ fontWeight: "bold" }} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button variant="contained" onClick={handleSelectAll} sx={{ fontWeight: "bold", fontSize: "1rem" }}>
          Select All Questions
        </Button>
        <Button variant="outlined" onClick={handleDeselectAll} sx={{ fontWeight: "bold", fontSize: "1rem" }}>
          Deselect All Questions
        </Button>
      </Box>

      {/* Main Table with horizontal bar chart effect and interactive hover */}
      <TableContainer component={Paper} sx={{ maxWidth: 1000, mx: "auto", mb: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold", fontSize: "1.1rem" }}>Model</TableCell>
              <TableCell align="right" sx={{ fontWeight: "bold", fontSize: "1.1rem" }}>
                Total
              </TableCell>
              <TableCell align="right" sx={{ fontWeight: "bold", fontSize: "1.1rem" }}>
                Coherence
              </TableCell>
              <TableCell align="right" sx={{ fontWeight: "bold", fontSize: "1.1rem" }}>
                Dissimilarity
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {modelsMetrics.map((model) => {
              const company = model.modelName.split("/")[0].toLowerCase();
              const rowColor = COMPANY_COLORS[company] || "#cccccc";
              const ratio = bestTotal ? (model.totalResponses / bestTotal) * 100 : 0;
              return (
                <TableRow
                  key={model.modelName}
                  hover
                  onClick={() => handleModelClick(model.modelName)}
                  sx={{
                    cursor: "pointer",
                    transition: "transform 0.2s ease, box-shadow 0.2s ease",
                    // Linear gradient bar effect: colored portion proportional to totalResponses.
                    background: `linear-gradient(to right, ${rowColor} ${ratio}%, white ${ratio}%)`,
                    ":hover": {
                      transform: "scale(1.02)",
                      boxShadow: 3,
                    },
                  }}
                >
                  <TableCell sx={{ fontWeight: "bold", fontSize: "1rem" }} component="th" scope="row">
                    {model.modelName}
                  </TableCell>
                  <TableCell align="right" sx={{ fontWeight: "bold", fontSize: "1rem" }}>
                    {model.totalResponses}
                  </TableCell>
                  <TableCell align="right" sx={{ fontWeight: "bold", fontSize: "1rem" }}>
                    {model.totalCoherence}
                  </TableCell>
                  <TableCell align="right" sx={{ fontWeight: "bold", fontSize: "1rem" }}>
                    {model.totalDissimilarity}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Modal for detailed model view (normal font weight) */}
      <Modal open={modalOpen} onClose={handleClose}>
        <Box sx={modalStyle}>
          <Typography variant="h5" gutterBottom sx={{ fontSize: "1.5rem" }}>
            Model: {selectedModelName}
          </Typography>
          {selectedModelDetail ? (
            Object.entries(selectedModelDetail).map(([paramKey, questions]) => (
              <Box key={paramKey} sx={{ mb: 4 }}>
                <Typography variant="subtitle1" color="text.secondary" sx={{ fontSize: "1.2rem" }}>
                  Parameter: {paramKey}
                </Typography>
                {Object.entries(questions).map(([question, responses]) => {
                  // Prepare chart data for this question
                  const chartData = {
                    labels: responses.map((r) => `#${r.answer_num}`),
                    datasets: [
                      {
                        label: "Coherence",
                        data: responses.map((r) => r.coherence_score),
                        borderColor: "#8884d8",
                        backgroundColor: "#8884d8",
                        fill: false,
                      },
                      {
                        label: "Dissimilarity (%)",
                        data: responses.map((r) =>
                          parseFloat((r.embedding_dissimilarity_score * 100).toFixed(1))
                        ),
                        borderColor: "#82ca9d",
                        backgroundColor: "#82ca9d",
                        fill: false,
                      },
                    ],
                  };

                  const chartOptions = {
                    responsive: true,
                    plugins: {
                      legend: {
                        position: "top",
                      },
                      title: {
                        display: true,
                        text: "Coherence & Dissimilarity vs Response Number",
                      },
                    },
                  };

                  return (
                    <Box key={question} sx={{ mt: 2, pl: 2, borderLeft: 2, borderColor: "grey.300", mb: 4 }}>
                      <Typography variant="body1" sx={{ fontSize: "1.1rem" }}>
                        {question}
                      </Typography>
                      {/* Chart below the question */}
                      <Box sx={{ maxWidth: 600, mx: "auto", my: 2 }}>
                        <Line data={chartData} options={chartOptions} />
                      </Box>
                      {responses.map((resp, idx) => (
                        <Box
                          key={idx}
                          sx={{
                            display: "flex",
                            alignItems: "center",
                            p: 1,
                            my: 1,
                            backgroundColor: "#f5f5f5",
                            borderRadius: 1,
                          }}
                        >
                          {/* Response number on the left */}
                          <Typography variant="body2" sx={{ width: "40px", mr: 1 }}>
                            #{resp.answer_num}
                          </Typography>
                          {/* Answer text */}
                          <Typography variant="body2" sx={{ flex: 1, mr: 2 }}>
                            {resp.answer}
                          </Typography>
                          {/* Scores in a table-like layout */}
                          <Box sx={{ display: "flex", gap: 4, minWidth: 150, textAlign: "right" }}>
                            <Typography variant="body2">
                              Coherence: {resp.coherence_score}
                            </Typography>
                            <Typography variant="body2">
                              Dissimilarity:{" "}
                              {parseFloat((resp.embedding_dissimilarity_score * 100).toFixed(1))}
                            </Typography>
                          </Box>
                        </Box>
                      ))}
                    </Box>
                  );
                })}
              </Box>
            ))
          ) : (
            <Typography sx={{ fontSize: "1rem" }}>
              No data available for this model.
            </Typography>
          )}
          <Box textAlign="right" mt={2}>
            <Button variant="contained" onClick={handleClose} sx={{ fontSize: "1rem" }}>
              Close
            </Button>
          </Box>
        </Box>
      </Modal>
    </Box>
  );
}

export default App;

