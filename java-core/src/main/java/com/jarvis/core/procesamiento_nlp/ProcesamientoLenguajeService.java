package com.jarvis.core.procesamiento_nlp;

import org.springframework.stereotype.Service;
import java.time.LocalTime;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Locale;
import java.util.Random;

@Service
public class ProcesamientoLenguajeService {

    private final Random random = new Random();

    private String pick(String... options) {
        return options[random.nextInt(options.length)];
    }

    public IntentResult parseIntent(String text) {
        if (text == null || text.isBlank()) {
            return new IntentResult("UNKNOWN_APP", null, pick(
                "No te entendí bien, ¿puedes repetirlo?",
                "Hmm, no capté eso. Inténtalo de nuevo.",
                "No escuché bien. Dilo otra vez, por favor."
            ));
        }

        String normalized = text.toLowerCase().trim()
            .replace("á", "a").replace("é", "e").replace("í", "i")
            .replace("ó", "o").replace("ú", "u");

        // 1. ABRIR APLICACIONES
        if (normalized.startsWith("abre ") || normalized.startsWith("abrir ")
            || normalized.startsWith("inicia ") || normalized.startsWith("iniciar ")
            || normalized.startsWith("lanza ") || normalized.startsWith("lanzar ")
            || normalized.startsWith("abre el ") || normalized.startsWith("pon ")
            || normalized.startsWith("ejecuta ")) {

            String target = normalized
                .replaceFirst("^(abre|abrir|inicia|iniciar|lanza|lanzar|ejecuta|pon) ", "").trim();
            target = cleanArticles(target);

            if (target.contains("youtube") || target.contains("facebook") || target.contains("netflix")
                || target.contains("whatsapp") || target.contains("pagina") || target.contains("instagram")
                || target.contains("twitter") || target.contains("google") && target.contains("pagina")
                || target.contains("twitch") || target.contains("spotify") && target.contains("web")) {
                target = target.replace("la pagina de", "").replace("la web de", "").replace("la pagina", "").trim();
                return new IntentResult("OPEN_WEBSITE", target, pick(
                    "Enseguida, abriendo " + target + " en el navegador.",
                    "Voy a abrir " + target + " ahora mismo.",
                    "Abriendo " + target + " para ti."
                ));
            }
            return new IntentResult("OPEN_APP", target, pick(
                "Claro que sí, abriendo " + target + " ahora.",
                "Entendido, voy con " + target + ".",
                "En un momento te abro " + target + "."
            ));

        // 2. CERRAR APLICACIONES
        } else if (normalized.startsWith("cierra ") || normalized.startsWith("cerrar ")
            || normalized.startsWith("mata ") || normalized.startsWith("termina ")) {
            String target = normalized.replaceFirst("^(cierra|cerrar|mata|termina) ", "").trim();
            target = cleanArticles(target);
            return new IntentResult("CLOSE_APP", target, pick(
                "Cerrando " + target + " ahora mismo.",
                "De acuerdo, cierro " + target + ".",
                "Entendido, terminando " + target + "."
            ));

        // 3. MINIMIZAR
        } else if (normalized.startsWith("minimiza ") || normalized.startsWith("minimizar ")
            || normalized.startsWith("oculta ")) {
            String target = normalized.replaceFirst("^(minimiza|minimizar|oculta) ", "").trim();
            target = cleanArticles(target);
            return new IntentResult("MINIMIZE_APP", target, pick(
                "Minimizando " + target + ".",
                "Listo, escondo la ventana de " + target + "."
            ));

        // 4. MAXIMIZAR
        } else if (normalized.startsWith("maximiza ") || normalized.startsWith("maximizar ")
            || normalized.startsWith("restaura ") || normalized.startsWith("muestra ")) {
            String target = normalized.replaceFirst("^(maximiza|maximizar|restaura|muestra) ", "").trim();
            target = cleanArticles(target);
            return new IntentResult("MAXIMIZE_APP", target, pick(
                "Maximizando " + target + ".",
                "Trayendo " + target + " al frente."
            ));

        // 5. BUSCAR EN GOOGLE
        } else if (normalized.contains("busca en google ") || normalized.contains("buscar en google ")
            || normalized.contains("googlea ") || normalized.contains("busca en internet ")) {
            String target = normalized
                .replaceFirst("^.*(busca en google|buscar en google|googlea|busca en internet) ", "").trim();
            return new IntentResult("BROWSER_SEARCH", target, pick(
                "Buscando \"" + target + "\" en Google ahora mismo.",
                "Voy a Google a buscar " + target + ".",
                "Dame un segundo, busco " + target + " en Google."
            ));

        // 6. BUSCAR EN YOUTUBE
        } else if (normalized.contains("busca en youtube ") || normalized.contains("buscar en youtube ")
            || normalized.contains("pon en youtube ") || normalized.contains("busca youtube ")) {
            String target = normalized
                .replaceFirst("^.*(busca en youtube|buscar en youtube|pon en youtube|busca youtube) ", "").trim();
            return new IntentResult("YOUTUBE_SEARCH", target, pick(
                "Buscando \"" + target + "\" en YouTube.",
                "Voy a YouTube a buscar " + target + ".",
                "¡Vamos a YouTube! Buscando " + target + "."
            ));

        // 7. SUBIR VOLUMEN
        } else if (normalized.contains("sube el volumen") || normalized.contains("sube el son")
            || normalized.contains("mas volumen") || normalized.contains("sube el audio")
            || normalized.contains("mas audio") || normalized.contains("aumenta el volumen")) {
            return new IntentResult("VOLUME_UP", null, pick(
                "Subiendo el volumen.",
                "Voy a subir el sonido.",
                "Más volumen, entendido."
            ));

        // 8. BAJAR VOLUMEN
        } else if (normalized.contains("baja el volumen") || normalized.contains("baja el son")
            || normalized.contains("menos volumen") || normalized.contains("baja el audio")
            || normalized.contains("menos audio") || normalized.contains("reduce el volumen")) {
            return new IntentResult("VOLUME_DOWN", null, pick(
                "Bajando el volumen.",
                "De acuerdo, menos sonido.",
                "Bajando el audio ahora."
            ));

        // 9. SILENCIAR
        } else if (normalized.contains("silencia") || normalized.contains("mute")
            || normalized.contains("quitar volumen") || normalized.contains("sin sonido")
            || normalized.contains("modo silencio") || normalized.contains("acalla")) {
            return new IntentResult("VOLUME_MUTE", null, pick(
                "Silenciando el sistema.",
                "Modo silencio activado.",
                "Silencio total."
            ));

        // 10. REPRODUCIR / PAUSAR MÚSICA
        } else if (normalized.contains("pausa") || normalized.contains("reproduce")
            || normalized.contains("pon musica") || normalized.contains("play")
            || normalized.contains("pon la musica") || normalized.contains("reanuda")) {
            return new IntentResult("MEDIA_PLAY_PAUSE", null, pick(
                "Controlando la reproducción.",
                "Hecho.",
                "Play o pausa, como prefieras."
            ));

        // 11. SIGUIENTE CANCIÓN
        } else if (normalized.contains("siguiente") || normalized.contains("otra cancion")
            || normalized.contains("salta") || normalized.contains("skip")
            || normalized.contains("cambia la cancion") || normalized.contains("la que sigue")) {
            return new IntentResult("MEDIA_NEXT", null, pick(
                "Siguiente canción.",
                "Pasando a la siguiente pista.",
                "Cambiando de canción."
            ));

        // 12. CANCIÓN ANTERIOR
        } else if (normalized.contains("anterior") || normalized.contains("regresa la cancion")
            || normalized.contains("la anterior") || normalized.contains("vuelve la cancion")) {
            return new IntentResult("MEDIA_PREV", null, pick(
                "Regresando a la pista anterior.",
                "Volviendo a la canción anterior.",
                "Atrás."
            ));

        // 13. BLOQUEAR PANTALLA
        } else if (normalized.contains("bloquea la pantalla") || normalized.contains("bloquea el equipo")
            || normalized.contains("bloquea el pc") || normalized.contains("bloquear pantalla")
            || normalized.contains("bloquear equipo") || normalized.contains("cierra sesion")) {
            return new IntentResult("LOCK_SCREEN", null, pick(
                "Bloqueando el equipo. ¡Hasta luego!",
                "Pantalla bloqueada. Cuídate.",
                "Cerrando sesión. Nos vemos."
            ));

        // 14. CAPTURA DE PANTALLA
        } else if (normalized.contains("captura de pantalla") || normalized.contains("screenshot")
            || normalized.contains("toma una foto") || normalized.contains("captura la pantalla")
            || normalized.contains("toma una captura")) {
            return new IntentResult("TAKE_SCREENSHOT", null, pick(
                "Captura guardada.",
                "Foto tomada, ya está guardada.",
                "Listo, capturé la pantalla."
            ));

        // 15. HORA
        } else if (normalized.contains("que hora es") || normalized.contains("la hora")
            || normalized.contains("dime la hora") || normalized.contains("que horas son")) {
            LocalTime now = LocalTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("h:mm a");
            String hora = now.format(formatter);
            return new IntentResult("SAY_TEXT", null, pick(
                "Son las " + hora + ".",
                "Ahora mismo son las " + hora + ".",
                "La hora exacta es las " + hora + "."
            ));

        // 16. FECHA
        } else if (normalized.contains("que dia es") || normalized.contains("la fecha")
            || normalized.contains("que fecha es") || normalized.contains("que dia es hoy")) {
            LocalDate today = LocalDate.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("d 'de' MMMM 'de' yyyy", new Locale("es", "ES"));
            String fecha = today.format(formatter);
            return new IntentResult("SAY_TEXT", null, pick(
                "Hoy es " + fecha + ".",
                "Estamos a " + fecha + ".",
                "La fecha de hoy es " + fecha + "."
            ));

        // 17. APRENDER ALIAS
        } else if (normalized.startsWith("aprende ") || normalized.startsWith("aprender ")
            || normalized.startsWith("recuerda que ") || normalized.startsWith("memoriza ")) {
            String raw = normalized.replaceFirst("^(aprende|aprender|recuerda que|memoriza) ", "").trim();
            return new IntentResult("LEARN_ALIAS", raw, pick(
                "Anotado, ya aprendí eso.",
                "Perfecto, lo memoricé.",
                "Listo, recordaré eso para la próxima."
            ));
        }

        // FALLBACK A INTELIGENCIA ARTIFICIAL (GEMINI)
        // En lugar de rechazar el comando, se lo pasamos a Python como CHAT_QUERY
        return new IntentResult("CHAT_QUERY", text, null);
    }

    private String cleanArticles(String target) {
        if (target == null) return null;
        for (String art : new String[]{"la ", "el ", "los ", "las ", "un ", "una "}) {
            if (target.startsWith(art)) return target.substring(art.length()).trim();
        }
        return target;
    }

    public static class IntentResult {
        private final String intent;
        private final String target;
        private final String ttsMessage;

        public IntentResult(String intent, String target, String ttsMessage) {
            this.intent = intent;
            this.target = target;
            this.ttsMessage = ttsMessage;
        }

        public String intent() { return intent; }
        public String target() { return target; }
        public String ttsMessage() { return ttsMessage; }
    }
}
