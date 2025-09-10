#!/bin/bash

# Script pour arrêter le projet Honeypot Attack Map
# Usage: ./scripts/docker-stop.sh [options]

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
    echo -e "${BLUE}  Honeypot Attack Map - Stop${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Arrêter tous les services
stop_all() {
    print_message "Arrêt de tous les services..."
    
    # Arrêter les services principaux
    docker-compose down 2>/dev/null || true
    docker-compose -f docker/docker-compose.dev.yml down 2>/dev/null || true
    docker-compose -f docker/docker-compose.prod.yml down 2>/dev/null || true
    
    print_message "Services arrêtés avec succès !"
}

# Arrêter et supprimer les volumes
stop_and_clean() {
    print_warning "ATTENTION: Cette action va supprimer toutes les données !"
    read -p "Êtes-vous sûr de vouloir continuer ? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_message "Arrêt des services et suppression des volumes..."
        
        docker-compose down -v 2>/dev/null || true
        docker-compose -f docker/docker-compose.dev.yml down -v 2>/dev/null || true
        docker-compose -f docker/docker-compose.prod.yml down -v 2>/dev/null || true
        
        print_message "Services arrêtés et volumes supprimés !"
    else
        print_message "Opération annulée."
    fi
}

# Nettoyer les images
clean_images() {
    print_message "Nettoyage des images Docker..."
    
    # Supprimer les images du projet
    docker images | grep honeypot | awk '{print $3}' | xargs docker rmi -f 2>/dev/null || true
    
    # Nettoyer les images inutilisées
    docker image prune -f
    
    print_message "Images nettoyées !"
}

# Nettoyer complètement
full_clean() {
    print_warning "ATTENTION: Cette action va supprimer TOUT (conteneurs, volumes, images) !"
    read -p "Êtes-vous sûr de vouloir continuer ? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_message "Nettoyage complet en cours..."
        
        # Arrêter et supprimer tout
        docker-compose down -v --rmi all 2>/dev/null || true
        docker-compose -f docker/docker-compose.dev.yml down -v --rmi all 2>/dev/null || true
        docker-compose -f docker/docker-compose.prod.yml down -v --rmi all 2>/dev/null || true
        
        # Nettoyer le système Docker
        docker system prune -a -f --volumes
        
        print_message "Nettoyage complet terminé !"
    else
        print_message "Opération annulée."
    fi
}

# Afficher le statut
show_status() {
    print_message "Statut des services:"
    docker-compose ps 2>/dev/null || echo "Aucun service en cours d'exécution."
}

# Afficher l'aide
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  (aucune)    - Arrêter tous les services"
    echo "  --clean     - Arrêter et supprimer les volumes"
    echo "  --images    - Nettoyer les images Docker"
    echo "  --full      - Nettoyage complet (conteneurs + volumes + images)"
    echo "  --status    - Afficher le statut des services"
    echo "  --help      - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0              # Arrêter les services"
    echo "  $0 --clean      # Arrêter et supprimer les données"
    echo "  $0 --full       # Nettoyage complet"
}

# Fonction principale
main() {
    print_header
    
    case ${1:-""} in
        "--clean")
            stop_and_clean
            ;;
        "--images")
            stop_all
            clean_images
            ;;
        "--full")
            full_clean
            ;;
        "--status")
            show_status
            ;;
        "--help"|"-h")
            show_help
            ;;
        "")
            stop_all
            ;;
        *)
            print_error "Option non reconnue: $1"
            show_help
            exit 1
            ;;
    esac
}

# Exécuter la fonction principale
main "$@"
