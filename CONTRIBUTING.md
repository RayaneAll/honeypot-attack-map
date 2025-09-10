# Contributing to Honeypot Attack Map

Thank you for your interest in contributing to the Honeypot Attack Map project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Check existing issues** - Make sure the issue hasn't been reported already
2. **Use the issue template** - Provide clear description, steps to reproduce, and expected behavior
3. **Include system information** - OS, Docker version, browser, etc.
4. **Add screenshots** - If applicable, include screenshots or error messages

### Suggesting Features

1. **Check the roadmap** - See if the feature is already planned
2. **Open a feature request** - Use the feature request template
3. **Provide use cases** - Explain why this feature would be valuable
4. **Consider implementation** - If you have ideas on how to implement it

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** - `git checkout -b feature/amazing-feature`
3. **Make your changes** - Follow the coding standards
4. **Add tests** - Ensure your code is tested
5. **Update documentation** - Keep docs up to date
6. **Submit a pull request** - Use the PR template

## 📋 Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 18+
- Git

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/your-username/honeypot-attack-map.git
cd honeypot-attack-map
```

2. **Start development environment**
```bash
./scripts/docker-start.sh dev
```

3. **Make your changes**
4. **Test your changes**
```bash
# Backend tests
docker-compose exec backend python -m pytest tests/

# Frontend tests
docker-compose exec frontend npm test
```

## 🎨 Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Use meaningful variable and function names
- Keep functions small and focused

```python
def process_attack_data(attack: Attack) -> Dict[str, Any]:
    """
    Process attack data for API response.
    
    Args:
        attack: Attack object to process
        
    Returns:
        Dictionary containing processed attack data
    """
    return {
        "id": attack.id,
        "ip_address": attack.ip_address,
        "risk_level": attack.get_risk_level()
    }
```

### JavaScript/React (Frontend)

- Use ESLint configuration
- Follow React best practices
- Use functional components with hooks
- Use TypeScript where possible
- Write meaningful component names

```jsx
const AttackMap = ({ attacks, onAttackClick }) => {
  const [selectedAttack, setSelectedAttack] = useState(null);
  
  const handleMarkerClick = (attack) => {
    setSelectedAttack(attack);
    onAttackClick?.(attack);
  };
  
  return (
    <MapContainer center={[20, 0]} zoom={2}>
      {attacks.map(attack => (
        <AttackMarker
          key={attack.id}
          attack={attack}
          onClick={handleMarkerClick}
        />
      ))}
    </MapContainer>
  );
};
```

### CSS/Styling

- Use TailwindCSS utility classes
- Follow mobile-first responsive design
- Use consistent spacing and colors
- Write custom CSS only when necessary

```css
.attack-marker {
  @apply w-4 h-4 rounded-full border-2 border-white shadow-lg;
  animation: pulse 2s infinite;
}
```

## 🧪 Testing

### Backend Testing

- Write unit tests for all functions
- Test API endpoints with different scenarios
- Mock external dependencies
- Test error handling

```python
def test_attack_creation():
    """Test creating a new attack."""
    attack_data = {
        "ip_address": "192.168.1.1",
        "port": 22,
        "protocol": "SSH"
    }
    
    attack = Attack(**attack_data)
    assert attack.ip_address == "192.168.1.1"
    assert attack.port == 22
    assert attack.protocol == "SSH"
```

### Frontend Testing

- Test component rendering
- Test user interactions
- Test API integration
- Test responsive design

```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import AttackMap from './AttackMap';

test('renders attack map with markers', () => {
  const attacks = [
    { id: 1, ip_address: '192.168.1.1', latitude: 40.7128, longitude: -74.0060 }
  ];
  
  render(<AttackMap attacks={attacks} />);
  
  expect(screen.getByRole('img')).toBeInTheDocument();
});
```

## 📝 Documentation

### Code Documentation

- Write clear docstrings
- Add inline comments for complex logic
- Update README files when needed
- Keep API documentation current

### User Documentation

- Write clear installation instructions
- Provide usage examples
- Document configuration options
- Include troubleshooting guides

## 🔄 Pull Request Process

### Before Submitting

1. **Run tests** - Ensure all tests pass
2. **Check linting** - Fix any linting errors
3. **Update documentation** - Keep docs current
4. **Test manually** - Verify functionality works
5. **Squash commits** - Clean up commit history

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Manual testing completed
- [ ] Screenshots included (if UI changes)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks** - CI/CD pipeline runs
2. **Code review** - Maintainers review code
3. **Testing** - Verify functionality
4. **Approval** - Maintainer approves PR
5. **Merge** - PR is merged to main branch

## 🐛 Bug Reports

### Before Reporting

1. **Check existing issues** - Search for similar problems
2. **Update to latest version** - Ensure you're on the latest release
3. **Test in clean environment** - Try with fresh Docker containers

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. macOS, Windows, Linux]
- Docker version: [e.g. 20.10.0]
- Browser: [e.g. Chrome, Firefox, Safari]

**Additional context**
Any other context about the problem.
```

## 💡 Feature Requests

### Before Requesting

1. **Check roadmap** - See if already planned
2. **Search issues** - Look for similar requests
3. **Consider implementation** - Think about complexity

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

### Release Checklist

1. **Update version numbers**
2. **Update CHANGELOG.md**
3. **Run full test suite**
4. **Create release notes**
5. **Tag release**
6. **Deploy to production**

## 📞 Getting Help

### Community Support

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Discord** - For real-time chat (if available)

### Contact Maintainers

- **Email** - support@honeypot-attack-map.com
- **GitHub** - @maintainer-username

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- GitHub contributors page

Thank you for contributing to Honeypot Attack Map! 🛡️
