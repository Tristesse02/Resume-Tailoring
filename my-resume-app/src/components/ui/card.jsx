import styles from "./index.module.css";

export function Card({ children }) {
  return (
    <div className={styles.card}>{children}</div>
  );
}

export default function CardContent({ children }) {
  return <div className={styles.cardContent}>{children}</div>;
}
