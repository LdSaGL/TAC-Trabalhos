const express = require("express");
const { mongoose } = require("mongoose");

const app = express();
app.use(express.static("public")); // Serve static files from the 'public' directory
app.use(express.json()); // Server to understand JSON requests

const PORT = 3000;
const MONGO_URL = process.env.MONGO_URL;

// Schema and Model
const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: {
    type: String,
    enum: ["admin", "user"],
    required: true,
    default: "user",
  },
});

const User = mongoose.model("User", userSchema);

// Connect to MongoDB
async function connectDB() {
  try {
    await mongoose.connect(MONGO_URL);
    console.log("Connected to MongoDB");

    // Seeding with model
    const adminUser = await User.findOne({ username: "admin" }); // Important for the vulnerability
    if (!adminUser) {
      await User.create({
        username: "admin",
        password: "admin123",
        role: "admin",
      });
      console.log("Admin user created");
    }
  } catch (error) {
    console.error("MongoDB connection error:", error);
    process.exit(1);
  }
}

// Login route
app.post("/login", async (req, res) => {
  const userInput = req.body;
  console.log(
    `App [webapp]: Recebida tentativa de login com o objeto:`,
    userInput
  );
  try {
    // The vulnerability is the same: we pass the user's input directly to the query.
    const user = await User.findOne(userInput);

    if (user) {
      res.status(200).json({
        message: "Successful login",
        user: user.username,
        role: user.role,
      });
    } else {
      res.status(401).json({ message: "Invalid credentials" });
    }
  } catch (err) {
    res.status(500).json({ message: "Erro in the server", error: err.message });
  }
});

// Connect to MongoDB and start the server
connectDB().then(() => {
  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
  });
});
