import { createClient } from "redis";
const redisClient = createClient({
    url: process.env.REDIS_URL,
});
redisClient.on("clientError", (error) => {
    console.error("Redis Client Error", error);
});
await redisClient.connect();
export { redisClient };
