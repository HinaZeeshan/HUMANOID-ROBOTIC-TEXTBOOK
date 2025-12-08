import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    '01-ros2-basics',
    '02-urdf-models',
    '03-digital-twins',
    '04-nvidia-isaac',
    '05-vla-models',
    '06-humanoid-kinematics',
    '07-motion-planning',
    '08-capstone-project',
    {
      type: 'category',
      label: 'Tutorial - Basics',
      items: [
        'tutorial-basics/create-a-document',
        'tutorial-basics/create-a-blog-post',
        'tutorial-basics/create-a-page',
        'tutorial-basics/deploy-your-site',
        'tutorial-basics/congratulations',
      ],
    },
    {
        type: 'category',
        label: 'Tutorial - Extras',
        items: [
            'tutorial-extras/manage-docs-versions',
            'tutorial-extras/translate-your-site',
        ]
    }
  ],
};

export default sidebars;
