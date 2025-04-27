import { createClient } from "redis";

const redisClient = createClient({
  url: process.env.REDIS_URL, //'redis://localhost:6379'
});

redisClient.on("clientError", (error) => {
  console.error("Redis Client Error", error);
})

await redisClient.connect();

export { redisClient };