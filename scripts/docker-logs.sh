#!/bin/bash

# Script pour afficher les logs du projet Honeypot Attack Map
# Usage: ./scripts/docker-logs.sh [service] [options]

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Honeypot Attack Map - Logs${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Afficher les logs de tous les services
show_all_logs() {
    print_message "Affichage des logs de tous les services (Ctrl+C pour arrêter)..."
    docker-compose logs -f
}

# Afficher les logs d'un service spécifique
show_service_logs() {
    local service=$1
    print_message "Affichage des logs du service: $service (Ctrl+C pour arrêter)..."
    docker-compose logs -f "$service"
}

# Afficher les logs avec timestamps
show_logs_with_timestamps() {
    local service=${1:-""}
    if [ -n "$service" ]; then
        print_message "Affichage des logs du service: $service avec timestamps (Ctrl+C pour arrêter)..."
        docker-compose logs -f -t "$service"
    else
        print_message "Affichage des logs de tous les services avec timestamps (Ctrl+C pour arrêter)..."
        docker-compose logs -f -t
    fi
}

# Afficher les dernières lignes des logs
show_tail_logs() {
    local service=${1:-""}
    local lines=${2:-100}
    
    if [ -n "$service" ]; then
        print_message "Affichage des $lines dernières lignes du service: $service"
        docker-compose logs --tail="$lines" "$service"
    else
        print_message "Affichage des $lines dernières lignes de tous les services"
        docker-compose logs --tail="$lines"
    fi
}

# Afficher les logs d'erreur uniquement
show_error_logs() {
    local service=${1:-""}
    if [ -n "$service" ]; then
        print_message "Affichage des logs d'erreur du service: $service"
        docker-compose logs "$service" 2>&1 | grep -i error
    else
        print_message "Affichage des logs d'erreur de tous les services"
        docker-compose logs 2>&1 | grep -i error
    fi
}

# Afficher les logs de démarrage
show_startup_logs() {
    local service=${1:-""}
    if [ -n "$service" ]; then
        print_message "Affichage des logs de démarrage du service: $service"
        docker-compose logs --tail=50 "$service" | grep -i -E "(start|ready|listening|running)"
    else
        print_message "Affichage des logs de démarrage de tous les services"
        docker-compose logs --tail=50 | grep -i -E "(start|ready|listening|running)"
    fi
}

# Afficher l'aide
show_help() {
    echo "Usage: $0 [service] [options]"
    echo ""
    echo "Services disponibles:"
    echo "  backend    - Logs du backend FastAPI"
    echo "  frontend   - Logs du frontend React"
    echo "  init-db    - Logs d'initialisation de la base de données"
    echo "  populate-data - Logs de génération des données de test"
    echo ""
    echo "Options:"
    echo "  --follow, -f     - Suivre les logs en temps réel (défaut)"
    echo "  --timestamps, -t - Afficher les timestamps"
    echo "  --tail N         - Afficher les N dernières lignes"
    echo "  --errors, -e     - Afficher uniquement les erreurs"
    echo "  --startup, -s    - Afficher les logs de démarrage"
    echo "  --help, -h       - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0                    # Logs de tous les services"
    echo "  $0 backend            # Logs du backend uniquement"
    echo "  $0 --tail 50          # 50 dernières lignes de tous les services"
    echo "  $0 backend --errors   # Erreurs du backend uniquement"
    echo "  $0 --timestamps       # Logs avec timestamps"
}

# Fonction principale
main() {
    print_header
    
    local service=""
    local follow=true
    local timestamps=false
    local tail_lines=""
    local errors_only=false
    local startup_only=false
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --follow|-f)
                follow=true
                shift
                ;;
            --timestamps|-t)
                timestamps=true
                shift
                ;;
            --tail)
                tail_lines="$2"
                follow=false
                shift 2
                ;;
            --errors|-e)
                errors_only=true
                follow=false
                shift
                ;;
            --startup|-s)
                startup_only=true
                follow=false
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            -*)
                print_error "Option non reconnue: $1"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$service" ]; then
                    service="$1"
                else
                    print_error "Trop d'arguments: $1"
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Vérifier si les services sont en cours d'exécution
    if ! docker-compose ps | grep -q "Up"; then
        print_warning "Aucun service n'est en cours d'exécution."
        print_message "Utilisez './scripts/docker-start.sh' pour démarrer les services."
        exit 1
    fi
    
    # Exécuter la commande appropriée
    if [ "$errors_only" = true ]; then
        show_error_logs "$service"
    elif [ "$startup_only" = true ]; then
        show_startup_logs "$service"
    elif [ -n "$tail_lines" ]; then
        show_tail_logs "$service" "$tail_lines"
    elif [ "$timestamps" = true ]; then
        show_logs_with_timestamps "$service"
    elif [ "$follow" = true ]; then
        if [ -n "$service" ]; then
            show_service_logs "$service"
        else
            show_all_logs
        fi
    else
        show_all_logs
    fi
}

# Exécuter la fonction principale
main "$@"
