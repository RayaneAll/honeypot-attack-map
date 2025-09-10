#!/bin/bash

# Script pour démarrer le projet Honeypot Attack Map avec Docker
# Usage: ./scripts/docker-start.sh [mode]
# Modes: dev, prod, demo

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
    echo -e "${BLUE}  Honeypot Attack Map - Docker${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Vérifier si Docker est installé
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
}

# Vérifier si le projet est dans le bon répertoire
check_project_structure() {
    if [ ! -f "docker/docker-compose.yml" ]; then
        print_error "Le fichier docker-compose.yml n'est pas trouvé. Assurez-vous d'être dans le répertoire racine du projet."
        exit 1
    fi
}

# Nettoyer les conteneurs existants
cleanup_existing() {
    print_message "Nettoyage des conteneurs existants..."
    docker-compose down 2>/dev/null || true
    docker-compose -f docker/docker-compose.dev.yml down 2>/dev/null || true
    docker-compose -f docker/docker-compose.prod.yml down 2>/dev/null || true
}

# Construire les images
build_images() {
    print_message "Construction des images Docker..."
    docker-compose build --no-cache
}

# Démarrer en mode développement
start_dev() {
    print_message "Démarrage en mode développement..."
    docker-compose -f docker/docker-compose.dev.yml up -d
    
    print_message "Attente du démarrage des services..."
    sleep 10
    
    print_message "Services démarrés avec succès !"
    print_message "Frontend: http://localhost:3000"
    print_message "Backend: http://localhost:8000"
    print_message "API Docs: http://localhost:8000/docs"
}

# Démarrer en mode production
start_prod() {
    print_message "Démarrage en mode production..."
    docker-compose up -d
    
    print_message "Attente du démarrage des services..."
    sleep 15
    
    print_message "Services démarrés avec succès !"
    print_message "Frontend: http://localhost:3000"
    print_message "Backend: http://localhost:8000"
    print_message "API Docs: http://localhost:8000/docs"
}

# Démarrer en mode démonstration
start_demo() {
    print_message "Démarrage en mode démonstration avec données de test..."
    docker-compose --profile demo up -d
    
    print_message "Attente du démarrage des services..."
    sleep 20
    
    print_message "Services démarrés avec succès !"
    print_message "Frontend: http://localhost:3000"
    print_message "Backend: http://localhost:8000"
    print_message "API Docs: http://localhost:8000/docs"
    print_warning "Des données de démonstration ont été générées automatiquement."
}

# Afficher le statut des services
show_status() {
    print_message "Statut des services:"
    docker-compose ps
}

# Afficher les logs
show_logs() {
    print_message "Logs des services (Ctrl+C pour arrêter):"
    docker-compose logs -f
}

# Fonction principale
main() {
    print_header
    
    # Vérifications préliminaires
    check_docker
    check_project_structure
    
    # Mode par défaut
    MODE=${1:-dev}
    
    case $MODE in
        "dev")
            cleanup_existing
            build_images
            start_dev
            ;;
        "prod")
            cleanup_existing
            build_images
            start_prod
            ;;
        "demo")
            cleanup_existing
            build_images
            start_demo
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "clean")
            cleanup_existing
            print_message "Nettoyage terminé."
            ;;
        *)
            print_error "Mode non reconnu: $MODE"
            echo "Usage: $0 [dev|prod|demo|status|logs|clean]"
            echo "  dev   - Mode développement (défaut)"
            echo "  prod  - Mode production"
            echo "  demo  - Mode démonstration avec données de test"
            echo "  status - Afficher le statut des services"
            echo "  logs  - Afficher les logs des services"
            echo "  clean - Nettoyer les conteneurs existants"
            exit 1
            ;;
    esac
}

# Exécuter la fonction principale
main "$@"
