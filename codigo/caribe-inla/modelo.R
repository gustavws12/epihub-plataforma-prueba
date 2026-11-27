# Modelo de ejemplo del equipo caribe: pronóstico SINTÉTICO en R base (no usa datos del SIVIGILA).
ref <- as.Date("2026-11-14")
cuantiles <- c(0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99)
entidades <- c("05", "08", "11", "13", "15", "17", "18", "19", "20", "23", "25", "27", "41", "44", "47", "50", "52", "54", "63", "66", "68", "70", "73", "76", "81", "85", "86", "88", "91", "94", "95", "97", "99", "08001", "13001", "47001", "76001", "76109")
set.seed(202)
filas <- list()
for (loc in entidades) {
  base <- runif(1, 5, 400)
  for (h in 1:12) {
    sd <- 0.3 + 0.04 * h
    filas[[length(filas) + 1]] <- data.frame(
      reference_date = format(ref), target = "case dengue", horizon = h, location = loc,
      target_end_date = format(ref + 7 * h), output_type = "quantile",
      output_type_id = cuantiles, value = round(base * exp(sd * qnorm(cuantiles)), 2))
  }
}
salida <- file.path("model-output", "caribe-inla", "2026-11-14-caribe-inla.csv")
dir.create(dirname(salida), recursive = TRUE, showWarnings = FALSE)
write.csv(do.call(rbind, filas), salida, row.names = FALSE, quote = FALSE)
cat("Escrito", salida, "\n")
